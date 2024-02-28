# =========================================================================
#  Calendar - Functional and imperative programming in Python
#
#  Module: test_driver.py
#  Created: 2008-10-07 by Peter Dalenius
#  Updated 2009-09-25 by Anders Haraldsson
#    Translated to Python in 2012 by Peter L-G
#    Translated to English in 2013 by Anders M.L.
#    Changes in 2020 by Jonas K (NamedTuple, type hints, ...)
#  Dependencies:
#    cal_abstraction.py
#    cal_booking.py
#    cal_output.py
# =========================================================================
from typing import Dict

# THIS FILE SHOULD NOT BE MODIFIED!
# Your own test cases are specified in lab8d.py, which *uses*
# the test functionality defined in this file.


from cal_ui import *
from settings import CHECK_AGAINST_FACIT

if CHECK_AGAINST_FACIT:
    try:
        from facit_la8_uppg import *
    except:
        print("*" * 100)
        print("*" * 100)
        print("Kan inte hitta facit; ändra CHECK_AGAINST_FACIT i test_driver.py till False")
        print("*" * 100)
        print("*" * 100)
        raise
else:
    from lab8b import *
    from lab8d import free_spans

# In the code below, we assume that the function that generates the set of
# free time spans (a time_spans object) is called free_spans. It is also
# assumed to be invoked by free_spans(cal_day, ts_start, ts_end), in that
# order. You may need to modify your code to conform to this standard.


# =========================================================================
#  1. Additional components
# =========================================================================

# The goal is to see if the free_spans function produces correct results.
# In order to simplify the specification of test cases, we provide a set of
# functions that convert human-readable descriptions of appointments and
# search spans during a day, into testable data (actual CalendarDay and
# TimeSpanSeq objects, for example).  We also provide some functions that
# verify that data has been created correctly.


def test_tss_order(tss: TimeSpanSeq) -> None:
    """
    Verify that the given TimeSpanSeq contains spans in temporal order,
    and signal an error otherwise
    """
    # At this point we don't have a complete test suite for the construction
    # and insertion of TimeSpan objects in a TimeSpanSeq.  Instead we *assume*
    # that TimeSpanSeq works properly, and if not, we signal an error
    # through an assertion.  Had this been a full test system for the
    # entire calendar, we should instead have had separate test cases for
    # TimeSpanSeq, with the ability to generate a list of test cases that pass
    # and don't pass.

    span_seq = [span for span in tss_iter_spans(tss)]
    if not span_seq:
        return

    # Generate pairs of (span, next span)
    span_pairs = zip(span_seq, span_seq[1:])
    for ts1, ts2 in span_pairs:
        assert time_precedes_or_equals(ts_start(ts1), ts_start(ts2)), (
            f"Error in TimeSpanSeq:  Spans are not inserted in correct temporal order: "
            f"{ts1} is before {ts2} in {span_seq}"
        )


# This function converts from the human-readable form ["13:15-15:00", ...] to
# corresponding TimeSpan(Seq) objects.
def test_strings_to_spans(seq: List[str]) -> TimeSpanSeq:
    tss = new_time_span_seq()
    for item in seq:
        times = item.split("-")
        start = new_time_from_string(times[0])
        end = new_time_from_string(times[1])
        span = new_time_span(start, end)
        tss = tss_plus_span(tss, span)

    # To be on the safe side: Are the inserted spans there, in the right order?
    test_tss_order(tss)
    span_seq = [span for span in tss_iter_spans(tss)]
    for item in seq:
        times = item.split("-")
        start = new_time_from_string(times[0])
        end = new_time_from_string(times[1])
        span = new_time_span(start, end)
        assert span in span_seq
    return tss


def test_time_spans_to_cd(day: Day, tss: TimeSpanSeq) -> CalendarDay:
    """
    Generate a CalendarDay with one test appointment for each TimeSpan in the
    given TimeSpanSeq.
    """
    ensure_type(tss, TimeSpanSeq)

    cd = new_calendar_day(day)
    for ts in tss_iter_spans(tss):  # type: TimeSpan
        cd = cd_plus_appointment(cd, new_appointment(ts, new_subject("Test")))

    return cd


def test_tss_equals(tss1: TimeSpanSeq, tss2: TimeSpanSeq) -> bool:
    """
    Returns true iff tss1 and tss2 contains the same time spans in the same order.
    """
    ensure_type(tss1, TimeSpanSeq)
    ensure_type(tss2, TimeSpanSeq)

    spans1 = [span for span in tss_iter_spans(tss1)]
    spans2 = [span for span in tss_iter_spans(tss2)]

    if len(spans1) != len(spans2):
        return False

    for index in range(len(spans1)):
        if not ts_equals(spans1[index], spans2[index]):
            return False

    return True


# =========================================================================
#  2. Building and using test cases
# =========================================================================


def store_test_case(
        test_cases: Dict[int, List],
        test_nr: int,
        start_str: str,
        end_str: str,
        booking_data: List[str],
        exp_result: List[str],
) -> None:
    """
    This function stores information about a single test case that the test case runner
    can execute.

    :param test_cases: The test case mapping where the test case is stored.
    :param test_nr:  The test number; this should uniquely identify the test case.
    :param start_str: The start of the search interval.
    :param end_str:  The end of the search interval.
    :param booking_data:  A list of appointment spans in text format (in the form "HH:MM-HH:MM")
    :param exp_result: A similar list of expected results
    """
    start = new_time_from_string(start_str)
    end = new_time_from_string(end_str)
    cal_day = test_time_spans_to_cd(new_day(1), test_strings_to_spans(booking_data))
    res_mts = test_strings_to_spans(exp_result)

    # The data generated is a test case (with a calendar day and a set of
    # expected time spans) that is added to the set of test cases.
    test_cases[test_nr] = [start, end, cal_day, res_mts]


def run_free_spans_tests(test_cases: dict):
    """
    Goes through the specified test cases and compares actual and expected output.
    """
    all_ok = True
    cases = 0
    for test_nr in test_cases:
        cases += 1
        current_case = test_cases[test_nr]
        start = current_case[0]
        end = current_case[1]
        cal_day = current_case[2]
        expected_results = current_case[3]

        if not test_tss_equals(free_spans(cal_day, start, end), expected_results):
            all_ok = False

            print("----")
            print(f"Test case {test_nr} generates unexpected output.")
            print("Free time spans:")
            show_time_spans(free_spans(cal_day, start, end))
            print()
            print("Expected:")
            show_time_spans(expected_results)
            print("----")
            print()

    if all_ok:
        print("All ({}) test cases OK.".format(cases))
