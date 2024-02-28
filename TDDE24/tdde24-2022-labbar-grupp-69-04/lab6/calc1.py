from calc import * 




def exec_program(code, dict = {}):
    """checks if "code" is a valid program"""
    if is_program(code):
        statements = program_statements(code)
        return exec_statements(statements, dict)
    else:
        raise KeyError("Can't interpret as a calc program.")


def exec_statements(statements, dict):
    """checks if statements is empty if it is it returns first statement again
    else returns rest of statements"""
    if empty_statements(statements):
        return dict

    first = exec_statement(first_statement(statements), dict)

    return exec_statements(rest_statements(statements), first)
    
def exec_statement(statement,dict):
    """checks what kind of statement it is"""
    if is_assignment(statement):
        return exec_assignment(statement, dict)

    if is_repetition(statement):
        return exec_repetition(statement , dict)

    if is_selection(statement):
        return exec_selection(statement , dict)

    if is_output(statement):
        return exec_output(statement , dict)

    if is_input(statement):
        return exec_input(statement, dict)

    else:
        raise SyntaxError
        
def exec_selection(p,dict):
    """checks a condition"""
    value = eval_condition(selection_condition(p), dict)

    if value:
        return exec_statement(selection_true_branch(p), dict)
    elif selection_has_false_branch(p):
        return exec_statement(selection_false_branch(p), dict)
    else:
        return dict

def exec_output(p, dict):
    """prints a statement"""
    out= output_expression(p)
    exp = eval_expression(out, dict)
    if is_variable(out):
        print(out, "=", exp)
        return dict
    else:
        print(exp)
        
def exec_assignment(p, dict):
    """calculates the value of a variable in a new dict"""
    dict_c = dict.copy()

    exp = eval_expression(assignment_expression(p), dict_c)
    var = assignment_variable(p)
    dict_c[var] = exp
    
    return dict_c

def exec_repetition(statement, dict):
    """Performs statement while condition is true kolla första return och copy"""
    while eval_condition(repetition_condition(statement), dict):
        dict = exec_statements(repetition_statements(statement), dict)
    return dict

    
def exec_input(p, dict):     
    """reads a variable"""
    dict_c = dict.copy()
    inp = input(f"Enter value for {input_variable(p)}: ")
    dict_c[input_variable(p)] = int(inp)
    return dict_c

def eval_condition(p, dict):
    """evaluates the type of condition"""
    left = eval_expression(condition_left(p), dict)
    right = eval_expression(condition_right(p), dict)
    operator = condition_operator(p)
    if operator == '=':
        return left == right
    if operator == '<':
        return left < right
    if operator == '>':
        return left > right

def eval_expression(p, dict):
    """checks if statement is a constant, a variable or binary"""
    if is_constant(p):
        return eval_constant(p)
    if is_variable(p):
        return eval_variable(p, dict)
    if is_binaryexpr(p):
        return eval_binaryexpr(p,dict)
    else:
        raise SyntaxError(str(p) + ": The given expression was \
            not a valid expression")

def eval_binaryexpr(p, dict):
    """evaluates the type of binary expression"""
    left = eval_expression(binaryexpr_left(p), dict)
    right = eval_expression(binaryexpr_right(p), dict)
    operator = binaryexpr_operator(p)
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "/":
        return left / right
    else:
        raise SyntaxError("Binary expression: Operator is not supported")


def eval_constant(con):
    """returns the value of a constant"""
    return con

def eval_variable(var, dict):
    """returns the value of the variable in dict"""
    
    return dict[var]


"""Tester som inte ska funka"""
calc1 = ['calc', ['set','x', '7'], ['print', 'x']] #Ska ge KeyError(assignar x till en sträng)
calc2 = ['kalk', ['if', [7, '<', 5], ['print', 2], ['print', 4]]] #Ska ge KeyError (inte calc)
calc3 = ['calc', ['set', 'a' , 5], ['print', '%&/']] #ska ge invalid syntax(printa något som inte är definerat)

"""Tester som ska funka"""
calc4 = ['calc', ['set','x', 7.2], ['print', 'x']] #Ska funka för float
calc5 = ['calc', ['read', 'n'], ['set', 'sum', 0], ['while', ['n', '>', 0], ['set', 'sum', ['sum', '+', 'n']], ['set', 'n', ['n', '-', 1]]], ['print', 'sum']] #Repetition ska funka

exec_program(calc4)