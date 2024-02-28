# =========================================================================
#  The Calendar - Functional and imperative programming in Python
#
#  Module: cal_output.py
#  Updated: 2004-07-30 by Peter Dalenius
#    Translated to Python in 2012 by Peter L-G
#    Translated to English in 2013 by Anders M.L.
#    Changes in 2020 by Jonas K (NamedTuple, type hints, ...)
#  Dependencies:
#    cal_abstraction.py
# =========================================================================

from cal_abstraction import *


# =========================================================================
#  1. Printing simple datatypes
# =========================================================================
def show_hour(h: Hour) -> None:
    """Print the parameter in an appropriate way, with no line break."""
    print(h, end="")


def show_minute(m: Minute) -> None:
    """Print the parameter in an appropriate way, with no line break."""
    print(m, end="")


def show_day(d: Day) -> None:
    """Print the parameter in an appropriate way, with no line break."""
    print(day_number(d), end="")


def show_month(m: Month) -> None:
    """Print the parameter in an appropriate way, with no line break."""
    print(month_name(m), end="")


def show_subject(s: Subject) -> None:
    """Print the parameter in an appropriate way, with no line break."""
    print(subject_text(s), end="")


# =========================================================================
#  2. Printing compound datatypes
# =========================================================================
def show_duration(tr: Duration) -> None:
    """Print the parameter in an appropriate way, with no line break."""
    print(
        f"{duration_hour(tr)} hours, "
        f"{duration_minute(tr)} minutes"
    )


def show_time(t: Time) -> None:
    """Print the parameter in an appropriate way, with no line break."""
    # ...:02 prints two digits, beginning with 0 if the number is less than 10.
    print(
        f"{hour_number(time_hour(t)):02}:{minute_number(time_minute(t)):02}", end="",
    )


def show_ts(ts: TimeSpan) -> None:
    """Print the parameter in an appropriate way, with no line break."""
    show_time(ts_start(ts))
    print("-", end="")
    show_time(ts_end(ts))


def show_date(d: Date) -> None:
    """Print the parameter in an appropriate way, with no line break."""
    show_day(date_day(d))
    print(" ", end="")
    show_month(date_month(d))


def show_appointment(app: Appointment) -> None:
    """Print the parameter in an appropriate way, with no line break."""
    show_ts(app_span(app))
    print(" ", end="")
    show_subject(app_subject(app))


def show_cd(cal_day: CalendarDay) -> None:
    """Print the given calendar day, one appointment per line."""
    for appointment in cd_iter_appointments(cal_day):
        show_appointment(appointment)
        print()


# =========================================================================
#  3. Miscellaneous output functions
# =========================================================================
def show_day_heading(d: Day, m: Month) -> None:
    """Print an appropriate heading for the given day and month."""
    s = f"{day_number(d)} {month_name(m)}"
    print(s)
    print("=" * len(s))
