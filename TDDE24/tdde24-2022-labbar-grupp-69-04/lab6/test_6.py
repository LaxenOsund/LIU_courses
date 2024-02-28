#!/usr/bin/env python3
"""
A test unit for the calc interpreter.

Note:
If you have downloaded the scripts from the website it might not
have the access right. To solve this run:
$ chmod +x <path_to_test_6.py>

Usage:
$ ./test_6.py <path_to_lab>
or
$ ./test_6.py --test a <path_to_lab>
or
$ ./test_6.py --test A <path_to_lab>
to test lab 6B
$ ./test_6.py --test alt <path_to_lab>
or
$ ./test_6.py --test ALT <path_to_lab>
to test with alternative_calc.py, remember to import it instead of calc in the source

Initial version by Erik Hansson <erik.b.hansson@liu.se>

Changelog:
 * 31/8-2016: Updated the printed traceback in case that the given file
   can not be imported.
"""

from argparse import ArgumentParser
from importlib.machinery import SourceFileLoader
from traceback import format_exc
from unittest import TestCase, defaultTestLoader, TextTestRunner
import sys


def print_stdout(val):
    """
    Prints val to standard stdout
    """
    current_out = sys.stdout
    sys.stdout = sys.__stdout__
    print(val)
    sys.stdout = current_out


class InputGenerator:
    """
    An input class for creating inputs instead fo stdin
    """

    @staticmethod
    def generator(values):
        """
        Creates a generator that yields all the values as strings
        """
        for elem in values:
            yield (str(elem))

    def __init__(self, values=None):
        if values is not None:
            self._generator = InputGenerator.generator(values)
        else:
            self._generator = None

    def readline(self):
        """
        Reads one item from the generator or empty string if there is no
        generator.
        """
        if self._generator is not None:
            return self._generator.__next__()
        else:
            return ""

    def setInputFeed(self, values):
        """
        Sets the next inputs to be those of values.
        Note that this flushes the input stream.
        """
        self._generator = InputGenerator.generator(values)


class OutputObject:
    """
    A simple output class for capturing any prints
    """

    def __init__(self):
        self._output_queue = []
        self._string_buffer = ""

    def write(self, string):
        """
        Writes a string to the output buffer
        """
        while "\n" in string:
            self._string_buffer += string[: string.index("\n") + 1]
            self._output_queue.append(self._string_buffer)
            self._string_buffer = ""
            string = string[string.index("\n") + 1 :]
        self._string_buffer += string

    def readline(self):
        """
        Reads a line from the output queue or everything that is in the
        temporary string buffer if no new line has been written.
        """
        if len(self._output_queue) > 0:
            val = self._output_queue[0]
            self._output_queue = self._output_queue[1:]
        else:
            val = self._string_buffer
            self._string_buffer = ""
        return val

    def flush(self):
        """
        Sends the output string buffer to the output queue
        """
        self._output_queue.append(self._string_buffer)
        self._string_buffer = ""


class TestEvalProgram(TestCase):
    """
    A unit test for the eval program
    """

    _set_a_prog = ["calc", ["set", "a", 7]]
    _print_and_set_a_prog = ["calc", ["print", "a"], ["set", "a", 0]]
    _input_a_prog = ["calc", ["read", "a"]]
    _print_a_prog = ["calc", ["print", "a"]]
    _print_if_prog = ["calc", ["if", ["a", ">", "b"], ["print", "a"], ["print", "a"]]]
    _read_and_print_a_prog = ["calc", ["read", "a"], ["print", "a"]]
    _if_prog = [
        "calc",
        ["read", "x"],
        ["set", "zero", 0],
        ["set", "pos", 1],
        ["set", "nonpos", -1],
        ["if", ["x", "=", 0], ["print", "zero"]],
        ["if", ["x", ">", 0], ["print", "pos"]],
        ["if", ["x", "<", 0], ["print", "nonpos"]],
    ]
    _if_set_prog = [
        "calc",
        ["read", "x"],
        ["if", ["x", ">", 0], ["set", "a", 1], ["set", "a", -1]],
        ["if", ["x", "=", 0], ["set", "a", 0]],
    ]
    _loop_prog = [
        "calc",
        ["read", "n"],
        ["set", "sum", 0],
        [
            "while",
            ["n", ">", 0],
            ["set", "sum", ["sum", "+", "n"]],
            ["set", "n", ["n", "-", 1]],
        ],
        ["print", "sum"],
    ]
    _loop_with_binexpr_prog = [
        "calc",
        ["read", "n"],
        ["set", "sum", 0],
        [
            "while",
            [["n", "-", 1], ">", 0],
            ["set", "sum", ["sum", "+", "n"]],
            ["set", "n", ["n", "-", 1]],
        ],
        ["print", "sum"],
    ]

    def tearDown(self):
        """
        Restors the system input and output streams after the tests
        has been conducted
        """
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

    def setUp(self):
        """
        Creates some sample programs and rewrites the system
        output and input to buffer objects
        """
        self._input = InputGenerator()
        sys.stdin = self._input
        self._output = OutputObject()
        sys.stdout = self._output

    def testReturnValue(self):
        """
        Tests so that the returned variable table are correct
        """
        new_vars = lab6.exec_program(self._set_a_prog)
        self.assertEqual(new_vars, {"a": 7})
        self._input.setInputFeed([10])
        new_vars = lab6.exec_program(self._input_a_prog)
        self.assertEqual(new_vars, {"a": 10})

    def testDestructiveness(self):
        """
        Tests so that the function is not destructive
        """
        my_vars = {"a": 5}

        # Should deepcopy if necessary
        new_vars = lab6.exec_program(self._set_a_prog, my_vars)
        self.assertEqual(my_vars, {"a": 5})
        self.assertEqual(new_vars, {"a": 7})
        self.assertIsNot(my_vars, new_vars)

        # Should deepcopy if necessary
        self._input.setInputFeed([10])
        new_vars = lab6.exec_program(self._input_a_prog, my_vars)
        self.assertEqual(my_vars, {"a": 5})
        self.assertEqual(new_vars, {"a": 10})
        self.assertIsNot(my_vars, new_vars)

        # Should deepcopy if necessary
        new_vars = lab6.exec_program(self._print_and_set_a_prog, my_vars)
        self.assertEqual(my_vars, {"a": 5})
        self.assertEqual(new_vars, {"a": 0})
        self.assertIsNot(my_vars, new_vars)

        # Shouldn't deepcopy if this isn't necessary
        new_vars = lab6.exec_program(self._print_a_prog, my_vars)
        self.assertIs(my_vars, new_vars)

        # Shouldn't deepcopy if this isn't necessary
        my_vars = {"a": 5, "b": 10}
        new_vars = lab6.exec_program(self._print_if_prog, my_vars)
        self.assertIs(my_vars, new_vars)

    def testIO(self):
        """
        Tests simple input output functionality
        """
        self._input.setInputFeed([4])
        lab6.exec_program(self._read_and_print_a_prog)
        self.assertEqual(self._output.readline(), "Enter value for a: ")
        self.assertEqual(self._output.readline(), "a = 4\n")

    def testIf(self):
        """
        Tests the use of if-statements in calc
        """
        self._input.setInputFeed([-3, -1, 0, 1, 9])
        new_vars = lab6.exec_program(self._if_prog)
        self.assertEqual(new_vars, {"zero": 0, "pos": 1, "nonpos": -1, "x": -3})
        self.assertEqual(self._output.readline(), "Enter value for x: ")
        self.assertEqual(self._output.readline(), "nonpos = -1\n")
        new_vars = lab6.exec_program(self._if_prog)
        self.assertEqual(new_vars, {"zero": 0, "pos": 1, "nonpos": -1, "x": -1})
        self.assertEqual(self._output.readline(), "Enter value for x: ")
        self.assertEqual(self._output.readline(), "nonpos = -1\n")
        new_vars = lab6.exec_program(self._if_prog)
        self.assertEqual(new_vars, {"zero": 0, "pos": 1, "nonpos": -1, "x": 0})
        self.assertEqual(self._output.readline(), "Enter value for x: ")
        self.assertEqual(self._output.readline(), "zero = 0\n")
        new_vars = lab6.exec_program(self._if_prog)
        self.assertEqual(new_vars, {"zero": 0, "pos": 1, "nonpos": -1, "x": 1})
        self.assertEqual(self._output.readline(), "Enter value for x: ")
        self.assertEqual(self._output.readline(), "pos = 1\n")
        new_vars = lab6.exec_program(self._if_prog)
        self.assertEqual(new_vars, {"zero": 0, "pos": 1, "nonpos": -1, "x": 9})
        self.assertEqual(self._output.readline(), "Enter value for x: ")
        self.assertEqual(self._output.readline(), "pos = 1\n")

        # Test if_set
        self._input.setInputFeed([-3, 0, 1])
        new_vars = lab6.exec_program(self._if_set_prog)
        self.assertEqual(new_vars, {"x": -3, "a": -1})
        self.assertEqual(self._output.readline(), "Enter value for x: ")

        new_vars = lab6.exec_program(self._if_set_prog)
        self.assertEqual(new_vars, {"x": 0, "a": 0})
        self.assertEqual(self._output.readline(), "Enter value for x: ")

        new_vars = lab6.exec_program(self._if_set_prog)
        self.assertEqual(new_vars, {"x": 1, "a": 1})
        self.assertEqual(self._output.readline(), "Enter value for x: ")

    def testLoop(self):
        """
        Tests the use of loops in calc
        """
        self._input.setInputFeed([4, 1, 0, -1, 2])
        new_vars = lab6.exec_program(self._loop_prog)
        self.assertEqual(new_vars, {"n": 0, "sum": 10})
        self.assertEqual(self._output.readline(), "Enter value for n: ")
        self.assertEqual(self._output.readline(), "sum = 10\n")
        new_vars = lab6.exec_program(self._loop_prog)
        self.assertEqual(new_vars, {"n": 0, "sum": 1})
        self.assertEqual(self._output.readline(), "Enter value for n: ")
        self.assertEqual(self._output.readline(), "sum = 1\n")
        new_vars = lab6.exec_program(self._loop_prog)
        self.assertEqual(new_vars, {"n": 0, "sum": 0})
        self.assertEqual(self._output.readline(), "Enter value for n: ")
        self.assertEqual(self._output.readline(), "sum = 0\n")
        new_vars = lab6.exec_program(self._loop_prog)
        self.assertEqual(new_vars, {"n": -1, "sum": 0})
        self.assertEqual(self._output.readline(), "Enter value for n: ")
        self.assertEqual(self._output.readline(), "sum = 0\n")

        # Test once with an binary expression in the condition
        new_vars = lab6.exec_program(self._loop_with_binexpr_prog)
        self.assertEqual(new_vars, {"n": 1, "sum": 2})
        self.assertEqual(self._output.readline(), "Enter value for n: ")
        self.assertEqual(self._output.readline(), "sum = 2\n")


class TestAltEvalProgram(TestCase):
    """
    A unit test for the eval program, with the alternative Calc structure
    """

    _set_a_prog = {
        "type": "calc",
        "do": {"statements": [{"type": "set", "var": "a", "expr": 7}]},
    }
    _print_and_set_a_prog = {
        "type": "calc",
        "do": {
            "statements": [
                {"type": "print", "expr": "a"},
                {"type": "set", "var": "a", "expr": 0},
            ]
        },
    }
    _input_a_prog = {
        "type": "calc",
        "do": {"statements": [{"type": "read", "var": "a"}]},
    }
    _print_a_prog = {
        "type": "calc",
        "do": {"statements": [{"type": "print", "expr": "a"}]},
    }
    _print_if_prog = {
        "type": "calc",
        "do": {
            "statements": [
                {
                    "type": "if",
                    "cond": {"left": "a", "op": ">", "right": "b"},
                    "true": {"type": "print", "expr": "a"},
                    "false": {"type": "print", "expr": "a"},
                },
            ]
        },
    }
    _read_and_print_a_prog = {
        "type": "calc",
        "do": {
            "statements": [
                {"type": "read", "var": "a"},
                {"type": "print", "expr": "a"},
            ]
        },
    }
    _if_prog = {
        "type": "calc",
        "do": {
            "statements": [
                {"type": "read", "var": "x"},
                {"type": "set", "var": "zero", "expr": 0},
                {"type": "set", "var": "pos", "expr": 1},
                {"type": "set", "var": "nonpos", "expr": -1},
                {
                    "type": "if",
                    "cond": {"left": "x", "op": "=", "right": 0},
                    "true": {"type": "print", "expr": "zero"},
                },
                {
                    "type": "if",
                    "cond": {"left": "x", "op": ">", "right": 0},
                    "true": {"type": "print", "expr": "pos"},
                },
                {
                    "type": "if",
                    "cond": {"left": "x", "op": "<", "right": 0},
                    "true": {"type": "print", "expr": "nonpos"},
                },
            ]
        },
    }
    _if_set_prog = {
        "type": "calc",
        "do": {
            "statements": [
                {"type": "read", "var": "x"},
                {
                    "type": "if",
                    "cond": {"left": "x", "op": ">", "right": 0},
                    "true": {"type": "set", "var": "a", "expr": 1},
                    "false": {"type": "set", "var": "a", "expr": -1},
                },
                {
                    "type": "if",
                    "cond": {"left": "x", "op": "=", "right": 0},
                    "true": {"type": "set", "var": "a", "expr": 0},
                },
            ]
        },
    }
    _loop_with_binexpr_prog = {
        "type": "calc",
        "do": {
            "statements": [
                {"type": "read", "var": "n"},
                {"type": "set", "var": "sum", "expr": 0},
                {
                    "type": "while",
                    "cond": {
                        "left": {"left": "n", "op": "-", "right": 1},
                        "op": ">",
                        "right": 0,
                    },
                    "do": {
                        "statements": [
                            {
                                "type": "set",
                                "var": "sum",
                                "expr": {"left": "sum", "op": "+", "right": "n"},
                            },
                            {
                                "type": "set",
                                "var": "n",
                                "expr": {"left": "n", "op": "-", "right": 1},
                            },
                        ],
                    },
                },
                {"type": "print", "expr": "sum"},
            ]
        },
    }
    _loop_prog = {
        "type": "calc",
        "do": {
            "statements": [
                {"type": "read", "var": "n"},
                {"type": "set", "var": "sum", "expr": 0},
                {
                    "type": "while",
                    "cond": {"left": "n", "op": ">", "right": 0},
                    "do": {
                        "statements": [
                            {
                                "type": "set",
                                "var": "sum",
                                "expr": {"left": "sum", "op": "+", "right": "n"},
                            },
                            {
                                "type": "set",
                                "var": "n",
                                "expr": {"left": "n", "op": "-", "right": 1},
                            },
                        ],
                    },
                },
                {"type": "print", "expr": "sum"},
            ]
        },
    }

    def tearDown(self):
        """
        Restors the system input and output streams after the tests
        has been conducted
        """
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

    def setUp(self):
        """
        Creates some sample programs and rewrites the system
        output and input to buffer objects
        """
        self._input = InputGenerator()
        sys.stdin = self._input
        self._output = OutputObject()
        sys.stdout = self._output

    def testReturnValue(self):
        """
        Tests so that the returned variable table are correct
        """
        new_vars = lab6.exec_program(self._set_a_prog)
        self.assertEqual(new_vars, {"a": 7})
        self._input.setInputFeed([10])
        new_vars = lab6.exec_program(self._input_a_prog)
        self.assertEqual(new_vars, {"a": 10})

    def testDestructiveness(self):
        """
        Tests so that the function is not destructive
        """
        my_vars = {"a": 5}

        # Should deepcopy if necessary
        new_vars = lab6.exec_program(self._set_a_prog, my_vars)
        self.assertEqual(my_vars, {"a": 5})
        self.assertEqual(new_vars, {"a": 7})
        self.assertIsNot(my_vars, new_vars)

        # Should deepcopy if necessary
        self._input.setInputFeed([10])
        new_vars = lab6.exec_program(self._input_a_prog, my_vars)
        self.assertEqual(my_vars, {"a": 5})
        self.assertEqual(new_vars, {"a": 10})
        self.assertIsNot(my_vars, new_vars)

        # Should deepcopy if necessary
        new_vars = lab6.exec_program(self._print_and_set_a_prog, my_vars)
        self.assertEqual(my_vars, {"a": 5})
        self.assertEqual(new_vars, {"a": 0})
        self.assertIsNot(my_vars, new_vars)

        # Shouldn't deepcopy if this isn't necessary
        new_vars = lab6.exec_program(self._print_a_prog, my_vars)
        self.assertIs(my_vars, new_vars)

        # Shouldn't deepcopy if this isn't necessary
        my_vars = {"a": 5, "b": 10}
        new_vars = lab6.exec_program(self._print_if_prog, my_vars)
        self.assertIs(my_vars, new_vars)

    def testIO(self):
        """
        Tests simple input output functionality
        """
        self._input.setInputFeed([4])
        lab6.exec_program(self._read_and_print_a_prog)
        self.assertEqual(self._output.readline(), "Enter value for a: ")
        self.assertEqual(self._output.readline(), "a = 4\n")

    def testIf(self):
        """
        Tests the use of if-statements in calc
        """
        self._input.setInputFeed([-3, -1, 0, 1, 9])
        new_vars = lab6.exec_program(self._if_prog)
        self.assertEqual(new_vars, {"zero": 0, "pos": 1, "nonpos": -1, "x": -3})
        self.assertEqual(self._output.readline(), "Enter value for x: ")
        self.assertEqual(self._output.readline(), "nonpos = -1\n")
        new_vars = lab6.exec_program(self._if_prog)
        self.assertEqual(new_vars, {"zero": 0, "pos": 1, "nonpos": -1, "x": -1})
        self.assertEqual(self._output.readline(), "Enter value for x: ")
        self.assertEqual(self._output.readline(), "nonpos = -1\n")
        new_vars = lab6.exec_program(self._if_prog)
        self.assertEqual(new_vars, {"zero": 0, "pos": 1, "nonpos": -1, "x": 0})
        self.assertEqual(self._output.readline(), "Enter value for x: ")
        self.assertEqual(self._output.readline(), "zero = 0\n")
        new_vars = lab6.exec_program(self._if_prog)
        self.assertEqual(new_vars, {"zero": 0, "pos": 1, "nonpos": -1, "x": 1})
        self.assertEqual(self._output.readline(), "Enter value for x: ")
        self.assertEqual(self._output.readline(), "pos = 1\n")
        new_vars = lab6.exec_program(self._if_prog)
        self.assertEqual(new_vars, {"zero": 0, "pos": 1, "nonpos": -1, "x": 9})
        self.assertEqual(self._output.readline(), "Enter value for x: ")
        self.assertEqual(self._output.readline(), "pos = 1\n")

        # Test if_set
        self._input.setInputFeed([-3, 0, 1])
        new_vars = lab6.exec_program(self._if_set_prog)
        self.assertEqual(new_vars, {"x": -3, "a": -1})
        self.assertEqual(self._output.readline(), "Enter value for x: ")

        new_vars = lab6.exec_program(self._if_set_prog)
        self.assertEqual(new_vars, {"x": 0, "a": 0})
        self.assertEqual(self._output.readline(), "Enter value for x: ")

        new_vars = lab6.exec_program(self._if_set_prog)
        self.assertEqual(new_vars, {"x": 1, "a": 1})
        self.assertEqual(self._output.readline(), "Enter value for x: ")

    def testLoop(self):
        """
        Tests the use of loops in calc
        """
        self._input.setInputFeed([4, 1, 0, -1, 2])
        new_vars = lab6.exec_program(self._loop_prog)
        self.assertEqual(new_vars, {"n": 0, "sum": 10})
        self.assertEqual(self._output.readline(), "Enter value for n: ")
        self.assertEqual(self._output.readline(), "sum = 10\n")
        new_vars = lab6.exec_program(self._loop_prog)
        self.assertEqual(new_vars, {"n": 0, "sum": 1})
        self.assertEqual(self._output.readline(), "Enter value for n: ")
        self.assertEqual(self._output.readline(), "sum = 1\n")
        new_vars = lab6.exec_program(self._loop_prog)
        self.assertEqual(new_vars, {"n": 0, "sum": 0})
        self.assertEqual(self._output.readline(), "Enter value for n: ")
        self.assertEqual(self._output.readline(), "sum = 0\n")
        new_vars = lab6.exec_program(self._loop_prog)
        self.assertEqual(new_vars, {"n": -1, "sum": 0})
        self.assertEqual(self._output.readline(), "Enter value for n: ")
        self.assertEqual(self._output.readline(), "sum = 0\n")

        # Test once with an expression in the condition
        new_vars = lab6.exec_program(self._loop_with_binexpr_prog)
        self.assertEqual(new_vars, {"n": 1, "sum": 2})
        self.assertEqual(self._output.readline(), "Enter value for n: ")
        self.assertEqual(self._output.readline(), "sum = 2\n")


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "--test", choices=["a", "A", "alt", "ALT"], default="", required=False
    )
    arg_parser.add_argument("file")
    args = arg_parser.parse_args()
    if args.file.rfind("/") != -1:
        sys.path.append(args.file[: args.file.rfind("/")])
        potential_name = args.file[args.file.rfind("/") + 1 :]
    else:
        sys.path.append(".")
        potential_name = args.file
    if potential_name.rfind("."):
        name = potential_name[: potential_name.rfind(".")]
    else:
        name = potential_name
    try:
        lab6 = SourceFileLoader(name, args.file).load_module()
    except FileNotFoundError:
        print("Could not import lab: " + args.file)
        print("See traceback for further information:")
        print()
        stack_trace = format_exc().split("\n")
        importlib_has_started = False
        importlib_has_ended = False
        for line in stack_trace:
            if (
                not importlib_has_ended
                and importlib_has_started
                and line.lstrip().startswith("File")
                and "importlib" not in line
            ):
                importlib_has_ended = True
            if importlib_has_ended:
                print(line)
            elif (
                not importlib_has_started
                and line.lstrip().startswith("File")
                and "importlib" in line
            ):
                importlib_has_started = True
        exit(1)
    if args.test.upper() == "A" or args.test == "":
        res = (
            TextTestRunner(verbosity=2)
            .run(defaultTestLoader.loadTestsFromTestCase(TestEvalProgram))
            .wasSuccessful()
        )
    elif args.test.upper() == "ALT":
        res = (
            TextTestRunner(verbosity=2)
            .run(defaultTestLoader.loadTestsFromTestCase(TestAltEvalProgram))
            .wasSuccessful()
        )

    else:
        print("Unknown arguemnt for --test: " + args.test)
        exit(2)
    if res:
        print("The code passed all the tests")
