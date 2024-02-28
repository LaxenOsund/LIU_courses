# =========================================================================
#  Calendar - Functional and imperative programming in Python
#
#  Module: cal_abstraction.py
#  Updated: 2005-09-27 by Peter Dalenius
#    Translated to Python in 2012 by Peter L-G
#    Translated to English in 2013 by Anders M.L.
#    Changes in 2020 by Jonas K (NamedTuple, type hints, ...)
#  Dependencies:
#    None
# =========================================================================

# This module contains the definitions of the data types used by
# the calendar, including both the actual type definitions
# (usually using NamedTuple) and the low-level primitives that
# are used for manipulating the associated data.

# The module also contains a number of useful functions that are
# related to these datatypes, but that do not actually depend on
# how the datatypes are represented.  These should be clearly
# separated in the code below.

from typing import (
        Type, NamedTuple, List, Callable, Set, Dict, Any,
        get_origin, get_args
)

# =========================================================================
#  1. Basic functions for ensuring correctness.
# =========================================================================
from settings import USE_DEFAULT_DURATION_TYPE, USE_DEFAULT_TIMESPAN_TYPE


# =========================================================================
#  1. General machinery for testing types and other conditions.
# =========================================================================

def ensure(val, pred) -> None:
    """Assert that the given value satisfies the given predicate."""
    assert pred(val), f"Value {val} does not satisfy constraints."


def ensure_type(val, some_type: Type) -> None:
    """
        Assert that the given value is of the given type.

        Only handles X, List[X], Dict[X, Y]. Where X and Y are types handled by
        `ensure_type()` or are "simple" types.

        Some examples of "simple" types are: str, int, float, bool.
    """
    origin = get_origin(some_type)
    if origin is not None:
        # This is a nested type.
        assert type(val) is origin, f"Value {val} is of type {type(val)}; " \
                                    f"expected type {some_type}."
        args = get_args(some_type)
        if args and origin is list:
            element_type = args[0]
            for x in val:
                ensure_type(x, element_type)

        elif args and origin is dict:
            key_type, value_type = args
            for x in val.keys():
                ensure_type(x, key_type)

            for x in val.values():
                ensure_type(x, value_type)

        else:
            assert False, f"Cannot check the given type {some_type}"
    elif some_type is not Any:
        # 'Simple' type.
        assert type(val) is some_type, f"Value {val} is of type {type(val)}; " \
                                       f"expected type {some_type}."


# =========================================================================
#  2. Timepoints
# =========================================================================

# ----- HOUR -----

Hour = NamedTuple("Hour", [("number", int)])


def new_hour(number: int) -> Hour:
    """Create and return a new Hour with the given (non-negative) number."""
    ensure_type(number, int)

    # This is used both as a timepoint and as the length of an interval.
    # Therefore we should NOT test that the number of hours is at most 23.
    ensure(number, lambda h: 0 <= h)

    return Hour(number=number)


def hour_number(hour: Hour) -> int:
    """Return the number of the given Hour."""
    ensure_type(hour, Hour)
    return hour.number


# ----- MINUTE -----

Minute = NamedTuple("Minute", [("number", int)])


def new_minute(number: int) -> Minute:
    """Create and return a new Minute with the given (non-negative) number."""
    ensure_type(number, int)

    # This is used both as a timepoint and as the length of an interval.
    # Therefore we should NOT test that the number of minutes is at most 59.
    ensure(number, lambda m: 0 <= m)

    return Minute(number=number)


def minute_number(m: Minute) -> int:
    """Return the number of the given Minute."""
    ensure_type(m, Minute)
    return m.number


# ---- Time ----

Time = NamedTuple("Time", [("hour", Hour), ("minute", Minute)])


def new_time(hour: Hour, minute: Minute) -> Time:
    """
    Create and return a new Time with the given Hour and Minute, which
    must correspond to a valid 24-hour timepoint.
    """
    ensure_type(hour, Hour)
    ensure_type(minute, Minute)
    ensure(hour, lambda h: 0 <= hour_number(h) <= 23)
    ensure(minute, lambda m: 0 <= minute_number(m) <= 59)
    return Time(hour, minute)


def time_hour(time: Time) -> Hour:
    """Return the hour of a Time value"""
    ensure_type(time, Time)
    return time.hour


def time_minute(time: Time) -> Minute:
    """Return the minute of a Time value"""
    ensure_type(time, Time)
    return time.minute


# ---- Time: Functionality independent of the representation ----

def new_time_from_string(s: str) -> Time:
    """
    Create and return a new Time with the given Hour and Minute,
    given in the 5-character 'HH:MM' format (for example, '12:34')
    """
    hour = int(s[0:2])
    minute = int(s[3:5])
    return new_time(new_hour(hour), new_minute(minute))


def time_precedes(t1: Time, t2: Time) -> bool:
    """Return true iff t1 is strictly before t2"""
    hour1 = hour_number(time_hour(t1))
    hour2 = hour_number(time_hour(t2))
    min1 = minute_number(time_minute(t1))
    min2 = minute_number(time_minute(t2))
    return (hour1, min1) < (hour2, min2)


def time_equals(t1: Time, t2: Time) -> bool:
    """Return true iff t1 and t2 refer represent the same time."""
    hour1 = hour_number(time_hour(t1))
    hour2 = hour_number(time_hour(t2))
    min1 = minute_number(time_minute(t1))
    min2 = minute_number(time_minute(t2))
    return (hour1, min1) == (hour2, min2)


def time_precedes_or_equals(t1: Time, t2: Time) -> bool:
    """Return true iff t1 is before t2 or at the same time."""
    return time_precedes(t1, t2) or time_equals(t1, t2)


def time_latest(t1: Time, t2: Time) -> Time:
    """Return the later of two timepoints"""
    if time_precedes(t1, t2):
        return t2
    else:
        return t1


def time_earliest(t1: Time, t2: Time) -> Time:
    """Return the earliest of two timepoints"""
    if time_precedes(t1, t2):
        return t1
    else:
        return t2


# =========================================================================
#  4. Time spans (intervals) and their durations
# =========================================================================

# ---- TimeSpan ----

# TimeSpans have two different representations.

if USE_DEFAULT_TIMESPAN_TYPE:
    # We want to use the default implementation of the TimeSpan type, with
    # a NamedTuple having two fields called 'start' and 'end'.  Then we also
    # need the corresponding implementations of the lowest level functions
    # new_time_span(), ts_start(), and ts_end().  These are the only three
    # functions that should depend on the actual internal representation of
    # the TimeSpan type!
    TimeSpan = NamedTuple("TimeSpan", [("start", Time), ("end", Time)])


    def new_time_span(start: Time, end: Time) -> TimeSpan:
        """
        Create and return a new TimeSpan with the given start and end time.
        The start time must strictly precede the end time.
        """
        ensure_type(start, Time)
        ensure_type(end, Time)
        if time_equals(start, end):
            raise ValueError(f"Start and end time are the same, {start}, {end}.")
        elif not time_precedes(start, end):
            raise ValueError(f"Start time {start} must strictly precede the end time {end}.")
        else:
            return TimeSpan(start, end)


    def ts_start(ts: TimeSpan) -> Time:
        """Return the start of a TimeSpan"""
        ensure_type(ts, TimeSpan)
        return ts.start


    def ts_end(ts: TimeSpan) -> Time:
        """Return the end of a TimeSpan"""
        ensure_type(ts, TimeSpan)
        return ts.end

else:
    # We want to use an alternative dictionary-based representation for TimeSpans.
    # Again, we need to define TimeSpan and its three associated lower level
    # functions; as long as abstraction principles are followed correctly, we
    # should NOT need to change anything else.
    class TimeSpan(dict):
        """
        A dictionary representation of TimeSpans.
        """
        pass


    def new_time_span(start: Time, end: Time) -> TimeSpan:
        """
        Create and return a new TimeSpan with the given start and end time.
        The start time must strictly precede the end time.
        """
        ensure_type(start, Time)
        ensure_type(end, Time)
        if time_equals(start, end):
            raise ValueError(f"Start and end time are the same, {start}, {end}.")
        elif not time_precedes(start, end):
            raise ValueError(f"Start time {start} must strictly precede the end time {end}.")
        else:
            return TimeSpan(dict(start=start, end=end))


    def ts_start(ts: TimeSpan) -> Time:
        """Return the start of a TimeSpan"""
        ensure_type(ts, TimeSpan)
        return ts["start"]


    def ts_end(ts: TimeSpan) -> Time:
        """Return the end of a TimeSpan"""
        ensure_type(ts, TimeSpan)
        return ts["end"]

# ---- TimeSpan: Functionality independent of the representation ----

# Some functions from TimeSpan and Duration need to be modified in lab8a
# and are therefore placed in lab8a.py, so *this* file can remain unchanged.
# That file is imported later in this file.


# ---- Duration ----

if USE_DEFAULT_DURATION_TYPE:
    # We want to use the default implementation of the Duration type.
    # See also TimeSpan comments above.
    Duration = NamedTuple("Duration", [("hour", Hour), ("minute", Minute)])


    def new_duration(hour: Hour, minute: Minute) -> Duration:
        """Create a duration corresponding to given number of hours and minutes.
        You may specify more than 59 minutes; any multiple of 60 minutes will be
        converted to hours."""
        return Duration(Hour(hour_number(hour) + minute_number(minute) // 60),
                        Minute(minute_number(minute) % 60))


    def duration_hour(dur: Duration) -> Hour:
        """Return the number of whole hours in a Duration"""
        ensure_type(dur, Duration)
        return dur.hour


    def duration_minute(dur: Duration) -> Minute:
        """Return the number of minutes in a Duration
        (0 to 59, not including whole hours)"""
        ensure_type(dur, Duration)
        return dur.minute

else:
    # We want to use the alternative implementation of the Duration type.
    # See also TimeSpan comments above.

    Duration = NamedTuple("Duration", [("minutes", Minute)])


    def new_duration(hour: Hour, minute: Minute) -> Duration:
        """Create a duration corresponding to given number of hours and minutes.
        You may specify more than 59 minutes; any multiple of 60 minutes will be
        converted to hours."""
        return Duration(new_minute(hour_number(hour) * 60 + minute_number(minute)))


    def duration_hour(dur: Duration) -> Hour:
        """Return the number of whole hours in a Duration"""
        ensure_type(dur, Duration)
        return new_hour(minute_number(dur.minutes) // 60)


    def duration_minute(dur: Duration) -> Minute:
        """Return the number of minutes in a Duration
        (0 to 59, not including whole hours)"""
        ensure_type(dur, Duration)
        return new_minute(minute_number(dur.minutes) % 60)

# ---- Duration: Functionality independent of the representation ----

# Some functions from TimeSpan and Duration need to be modified in lab8a
# and are therefore placed in lab8a.py, so *this* file can remain unchanged.
#
# Yes, PEP8 says we shouldn't import anything in the middle of a file,
# but this lab is a special case that is quite different from actual
# production code.
from lab8a import *


def new_duration_from_string(s: str) -> Duration:
    """Create a duration corresponding to the string "HH:MM". The string must be
     well-formed and the number of hours can consist of an arbitrary number of digits."""
    pos = s.find(":")
    hour = int(s[0:pos])
    minute = int(s[pos + 1:])
    return new_duration(new_hour(hour), new_minute(minute))


# =========================================================================
#  5. Days, months and dates
# =========================================================================

# ---- Day ----

Day = NamedTuple("Day", [("number", int)])


def new_day(number: int) -> Day:
    """Create a Day (of the month) with the given number."""
    ensure_type(number, int)
    ensure(number, lambda d: 1 <= d <= 31)
    return Day(number=number)


def day_number(day: Day) -> int:
    """Return the day number of the given Day (of the month)."""
    ensure_type(day, Day)
    return day.number


# ---- Day: Functionality independent of the representation ----

# None at this point

# ---- Month ----

Month = NamedTuple("Month", [("name", str)])

# We ignore leap years here...
MONTHS = {
    ("jan", "january", 31, 1),
    ("feb", "february", 28, 2),
    ("mar", "march", 31, 3),
    ("apr", "april", 30, 4),
    ("may", "may", 31, 5),
    ("jun", "june", 30, 6),
    ("jul", "july", 31, 7),
    ("aug", "august", 31, 8),
    ("sep", "september", 30, 9),
    ("oct", "october", 31, 10),
    ("nov", "november", 30, 11),
    ("dec", "december", 31, 12),
}

# Using the specification above, we can easily create a number of associated sets
# and mappings/dictionaries...

MONTH_FULL_NAMES = {spec[1] for spec in MONTHS}  # type: Set[str]
MONTH_ABBREVIATIONS = {spec[0] for spec in MONTHS}  # type: Set[str]
MONTH_ABBREV_TO_NAME = {spec[0]: spec[1] for spec in MONTHS}  # type: Dict[str, str]
MONTH_NAME_TO_LENGTH = {spec[1]: spec[2] for spec in MONTHS}  # type: Dict[str, int]
MONTH_NAME_TO_NUMBER = {spec[1]: spec[3] for spec in MONTHS}  # type: Dict[str, int]


def new_month(name: str) -> Month:
    """Create and return a new Month with the given name.  The name must valid in English."""
    ensure_type(name, str)
    if name in MONTH_FULL_NAMES:
        return Month(name)
    elif name in MONTH_ABBREVIATIONS:
        return Month(MONTH_ABBREV_TO_NAME[name])
    else:
        raise ValueError(f"'{name}' is not the name of a month.")


ALL_MONTHS = [new_month(name) for name in MONTH_FULL_NAMES]  # type: List[Month]


def month_name(mon: Month) -> str:
    """Return the full English name of the given Month"""
    ensure_type(mon, Month)
    return mon.name


# ---- Month: Functionality independent of the representation ----


def month_number(mon: Month) -> int:
    """Return the number of the given Month (1 to 12)"""
    ensure_type(mon, Month)
    return MONTH_NAME_TO_NUMBER[month_name(mon)]


def days_in_month(mon: Month) -> int:
    """Return the number of days in the given Month, ignoring leap years."""
    ensure_type(mon, Month)
    return MONTH_NAME_TO_LENGTH[month_name(mon)]


# ----- Date -----

Date = NamedTuple("Date", [("day", Day), ("month", Month)])


def new_date(day: Day, mon: Month) -> Date:
    """Create and return a new Date with the given Day and Month."""
    ensure_type(day, Day)
    ensure_type(mon, Month)
    if day_number(day) > days_in_month(mon):
        raise ValueError(f"Date {day}, {mon} does not conform to specifications.")
    else:
        return Date(day, mon)


def date_month(date: Date) -> Month:
    """Return the Month of the given Date"""
    ensure_type(date, Date)
    return date.month


def date_day(date: Date) -> Day:
    """Return the Day of the given Date"""
    ensure_type(date, Date)
    return date.day


# =========================================================================
# 6. Appointments and their components.
# =========================================================================


# ----- SUBJECT -----


Subject = NamedTuple("Subject", [("text", str)])


def new_subject(text: str) -> Subject:
    """Create and return a new Subject with the given subject text."""
    ensure_type(text, str)
    return Subject(text)


def subject_text(subject: Subject) -> str:
    """Return the text of the given Subject"""
    ensure_type(subject, Subject)
    return subject.text


# ----- APPOINTMENT -----

Appointment = NamedTuple("Appointment", [("span", TimeSpan), ("subject", Subject)])


def new_appointment(span: TimeSpan, subject: Subject) -> Appointment:
    """Create and return a new Appointment with the given time span and subject."""
    ensure_type(span, TimeSpan)
    ensure_type(subject, Subject)
    return Appointment(span, subject)


def app_span(app: Appointment) -> TimeSpan:
    """Return the TimeSpan of the given Appointment"""
    ensure_type(app, Appointment)
    return app.span


def app_subject(app: Appointment) -> Subject:
    """Return the Subject of the given Appointment"""
    ensure_type(app, Appointment)
    return app.subject


# =========================================================================
#  7. Calendars -- days, months and years of *appointments*
# =========================================================================


# ----- CalendarDay -----

CalendarDay = NamedTuple(
    "CalendarDay", [("day", Day), ("appointments", List[Appointment])]
)


def new_calendar_day(day: Day, appointments: List[Appointment] = None) -> CalendarDay:
    """
    Create and return a new CalendarDay for the given Day of the month,
    with the given appointments.
    """
    ensure_type(day, Day)
    if appointments is None:
        # If we use [] as a default value above, then every call to this function will
        # use the *same* list as a default value.  Instead we must use None as
        # a value, and if something empty is provided, we create a *new* list each time.
        appointments = []
    else:
        ensure_type(appointments, List[Appointment])
    return CalendarDay(day, appointments)


def cd_day(cal_day: CalendarDay) -> Day:
    """Return the Day (of the month) of the given CalendarDay"""
    ensure_type(cal_day, CalendarDay)
    return cal_day.day


# We don't provide a way of retrieving the list of appointments.
# Instead, we provide a way of *iterating* over all appointments.

def cd_iter_appointments(cal_day: CalendarDay):
    """To be used as `for appointment in cd_iter_appointments(cal_day)"""
    # For the purpose of TDDE24, you do not necessarily have to know exactly how this works.
    # The point is that it gives others a way of iterating without knowing the internal
    # data structures.
    # If you are interested:  See "generator functions" at https://wiki.python.org/moin/Generators.
    ensure_type(cal_day, CalendarDay)
    for appointment in cal_day.appointments:
        yield appointment


def cd_is_empty(cal_day: CalendarDay) -> bool:
    """Return true iff the given CalendarDay has no appointments."""
    ensure_type(cal_day, CalendarDay)
    return not cal_day.appointments


def cd_plus_appointment(cal_day: CalendarDay, appointment: Appointment) -> CalendarDay:
    """
    Returns a copy of the given CalendarDay, where the given Appointment
    has been added in its proper position.
    """
    ensure_type(appointment, Appointment)
    ensure_type(cal_day, CalendarDay)

    def add_appointment(app: Appointment, appointments: List[Appointment]):
        if not appointments or time_precedes(
                ts_start(app_span(app)), ts_start(app_span(appointments[0]))
        ):
            return [app] + appointments
        else:
            return [appointments[0]] + add_appointment(app, appointments[1:])

    return new_calendar_day(
        cd_day(cal_day), add_appointment(appointment, cal_day.appointments)
    )


# ---- CalendarDay: Functionality independent of the representation ----


AppointmentPredicate = Callable[[Appointment], bool]
"""
This type corresponds to a *function* that takes an Appointment
as a parameter, and that returns a boolean value (True or False).
"""


def cd_any_appointment_satisfies(
        cal_day: CalendarDay, predicate: AppointmentPredicate
) -> bool:
    """
    Does any appointment during the given calendar day satisfy the
    given predicate?
    :param cal_day: A CalendarDay.
    :param predicate: A function that takes a particular Appointment
    as parameter and returns true iff the Appointment satisfies some
    condition.
    """
    ensure_type(cal_day, CalendarDay)
    return any(predicate(appointment)
               for appointment in cd_iter_appointments(cal_day))


# ----- CalendarMonth  -----

CalendarMonth = NamedTuple(
    "CalendarMonth", [("month", Month), ("days", List[CalendarDay])]
)
"""
A CalendarMonth contains zero or more CalendarDays containing Appointments.
The CalendarDays can be accessed ... +++
"""


# CalendarMonth currently happens to store CalendarDays in a list that is
# sorted on the day number (1 to 31).
#
# (This information belongs in a comment and NOT in a docstring, since it is
# just an explanation of how the *current* implementation works, not a
# promise that the user should count on!)


def new_calendar_month(month: Month, days: List[CalendarDay] = None) -> CalendarMonth:
    """
    Create and return a new CalendarMonth for the given month of the year,
    with the given list of CalendarDays.
    """
    ensure_type(month, Month)
    if days is None:
        # If we use [] as a default value above, then every call to this function will
        # use the *same* list as a default value.  Instead we must use None as
        # a value, and if something empty is provided, we create a *new* list each time.
        days = []
    else:
        ensure_type(days, List[CalendarDay])
    return CalendarMonth(month, days)


def cm_month(cal_month: CalendarMonth) -> Month:
    """Return the Month of the given CalendarMonth"""
    ensure_type(cal_month, CalendarMonth)
    return cal_month.month


def cm_iter_days(cal_mon: CalendarMonth):
    """To be used as `for cal_day in cm_iter_days(cal_month)`.     Iterates over all
    days in the month, not just those days that have appointments."""
    # For the purpose of TDDE24, you do not necessarily have to know exactly how this works.
    # The point is that it gives others a way of iterating without knowing the internal
    # data structures.
    # If you are interested:  See "generator functions" at https://wiki.python.org/moin/Generators.
    ensure_type(cal_mon, CalendarMonth)
    for daynum in range(1, days_in_month(cm_month(cal_mon)) + 1):
        yield cm_get_day(cal_mon, new_day(daynum))


def cm_is_empty(cal_mon: CalendarMonth) -> bool:
    """Return true iff the given CalendarMonth has no days."""
    ensure_type(cal_mon, CalendarMonth)
    return not cal_mon.days


def cm_plus_cd(cal_mon: CalendarMonth, cal_day: CalendarDay) -> CalendarMonth:
    """
    Returns a copy of the given CalendarMonth, where the given CalendarDay
    has been added in its proper position.  If the CalendarMonth already
    contains a CalendarDay for the same Day, then the old CalendarDay is
    replaced with the new CalendarDay.
    """
    ensure_type(cal_day, CalendarDay)
    ensure_type(cal_mon, CalendarMonth)

    def add_to(days: List[CalendarDay], day_to_add: CalendarDay) -> List[CalendarDay]:
        if not days:
            return [day_to_add]

        next_day = days[0]
        next_day_number = day_number(cd_day(next_day))

        daynum = day_number(cd_day(day_to_add))
        if daynum < next_day_number:
            # Add the new CalendarDay at the current position
            return [day_to_add] + days
        elif daynum == next_day_number:
            # Replace the CalendarDay at the current position with the new CalendarDay
            return [day_to_add] + days[1:]
        else:
            # Need to move further
            return [next_day] + add_to(days[1:], day_to_add)

    return CalendarMonth(cal_mon.month, add_to(cal_mon.days, cal_day))


def cm_last_booked_daynum(cal_mon: CalendarMonth) -> int:
    """
    Return the number of the last day-of-the-month that actually has an
    appointment in the given CalendarMonth, or 0 if there is no day
    with an appointment in this CalendarMonth.
    """
    ensure_type(cal_mon, CalendarMonth)
    if cm_is_empty(cal_mon):
        return 0
    else:
        # This is an internal CalendarMonth function that can use the structure directly.
        # We know that days are stored in order in cal_mon.days,
        # so we can simply pick the last one.
        last_cd = cal_mon.days[-1]
        # But we are NOT allowed to use the internal structure of CalendarDay
        # in this CalendarMonth-related function...
        last_day = cd_day(last_cd)
        return day_number(last_day)


def cm_get_day(cal_mon: CalendarMonth, day: Day) -> CalendarDay:
    """Return information about the given day of the given CalendarMonth."""
    ensure_type(day, Day)
    ensure_type(cal_mon, CalendarMonth)

    # Can't iterate using cm_iter_days(), because that function calls *us*!
    for cal_day in cal_mon.days:
        if cd_day(cal_day) == day:
            return cal_day

    # The CalendarMonth doesn't contain a CalendarDay for the given day,
    # so we create an empty one.
    # Since we are programming in a functional way, callers are not allowed
    # to modify the calendar month directly, so it doesn't matter that this
    # CalendarDay isn't actually stored in the CalendarMonth.
    return new_calendar_day(day)


# ----- CalendarYear -----

CalendarYear = NamedTuple("CalendarYear", [("months", List[CalendarMonth])])


def new_calendar_year(months: List[CalendarMonth] = None) -> CalendarYear:
    """
    Create and return a new CalendarYear for the given month of the year,
    with the given list of CalendarMonths.
    """
    if months is None:
        # If we use [] as a default value above, then every call to this function will
        # use the *same* list as a default value.  Instead we must use None as
        # a value, and if something empty is provided, the line below correctly
        # creates a *new* list each time.
        months = []
    else:
        ensure_type(months, List[CalendarMonth])
    return CalendarYear(months or [])


def cy_iter_months(cal_year: CalendarYear):
    """
    To be used as `for cal_month in cm_iter_months(cal_year)`.  Iterates over all
    12 months, not just those months that have appointments.
    """
    # For the purpose of TDDE24, you do not necessarily have to know exactly how this works.
    # The point is that it gives others a way of iterating without knowing the internal
    # data structures.
    # If you are interested:  See "generator functions" at https://wiki.python.org/moin/Generators.
    ensure_type(cal_year, CalendarYear)
    for month in ALL_MONTHS:
        yield cy_get_month(month, cal_year)


def cy_is_empty(cal_year: CalendarYear) -> bool:
    """Return true iff the given CalendarYear has no months."""
    ensure_type(cal_year, CalendarYear)
    return not cal_year.months


def cy_plus_cm(cal_year: CalendarYear, cal_mon: CalendarMonth) -> CalendarYear:
    """
    Returns a copy of the given CalendarYear, where the given CalendarMonth
    has been added in its proper position.  If the CalendarYear already
    contains a CalendarMonth for the same Month, then the old CalendarMonth is
    replaced with the new CalendarMonth.
    """
    ensure_type(cal_mon, CalendarMonth)
    ensure_type(cal_year, CalendarYear)

    month_to_insert = cm_month(cal_mon)

    def add_to(months: List[CalendarMonth], month_to_add: CalendarMonth) -> List[CalendarMonth]:
        if not months:
            return [month_to_add]

        next_month = months[0]
        next_month_number = month_number(cm_month(next_month))

        monthnum = month_number(cm_month(month_to_add))
        if monthnum < next_month_number:
            # Add the new CalendarMonth at the current position
            return [month_to_add] + months
        elif monthnum == next_month_number:
            # Replace the CalendarMonth at the current position with the new CalendarMonth
            return [month_to_add] + months[1:]
        else:
            # Need to move further
            return [next_month] + add_to(months[1:], month_to_add)

    if cm_is_empty(cal_mon):
        return cal_year
    elif cm_last_booked_daynum(cal_mon) > days_in_month(month_to_insert):
        raise ValueError(f"Too few days in {month_name(month_to_insert)}.")
    else:
        return CalendarYear(add_to(cal_year.months, cal_mon))


def cy_get_month(mon: Month, cal_year: CalendarYear) -> CalendarMonth:
    """Return information about the given month of the given CalendarYear."""
    ensure_type(mon, Month)
    ensure_type(cal_year, CalendarYear)

    # Can't iterate using cy_iter_months(), because that function calls *us*!
    for cal_month in cal_year.months:
        if cm_month(cal_month) == mon:
            return cal_month

    # The CalendarYear doesn't contain a CalendarMonth for the given month,
    # so we create an empty one.
    # Since we are programming in a functional way, callers are not allowed
    # to modify the calendar month directly, so it doesn't matter that this
    # CalendarMonth isn't actually stored in the CalendarYear.
    return new_calendar_month(mon)


# =========================================================================
#  8. A few tests.
# =========================================================================

# ---- ensure_type: A few simple tests ----


def test_ensure_type() -> None:
    """
    A few tests for ensure_type.
    """
    time1 = new_time_from_string("12:00")
    time2 = new_time_from_string("12:30")
    ensure_type(time1, Time)
    ensure_type([time1, time2], List[Time])
    ensure_type({"a": time1, "b": time2}, Dict[str, Time])
    ensure_type({"a": {1:1}, "b": {2:2}}, Dict[str, Dict[int, int]])
    ts = new_time_span(time1, time2)
    ensure_type(ts, TimeSpan)
    ensure_type([[ts]], List[List[TimeSpan]])
    ensure_type(1, Any)
    ensure_type([1, 2, "abc"], List[Any])

    def ensure_fail(*args):
        try:
            ensure_type(*args)
        except AssertionError:
            return
        assert False, f"ensure_type{args} should fail."

    ensure_fail(1, str)
    ensure_fail(1, List[Any])
    ensure_fail([1], List[str])
    ensure_fail([[[]], [1]], List[List[List[Any]]])
    ensure_fail([1, 2, "str"], List[int])

    print("ensure_type: All tests passed.")


# ---- Time: A few simple tests ----


def test_time() -> None:
    """
    A few simple tests for Time.
    """
    time1 = new_time_from_string("12:00")
    time2 = new_time_from_string("12:30")
    assert time_precedes(time1, time2)
    assert time_equals(time1, time1)
    assert time_precedes_or_equals(time1, time2)
    assert time_precedes_or_equals(time1, time1)
    assert not time_precedes_or_equals(time2, time1)
    assert hour_number(time_hour(time1)) == 12
    assert hour_number(time_hour(time2)) == 12
    assert minute_number(time_minute(time1)) == 0
    assert minute_number(time_minute(time2)) == 30

    print("test_time: All tests passed.")


# ---- TimeSpan: A few simple tests ----


def test_timespan_duration() -> None:
    """
    A few simple tests for lab 8A.  These tests don't necessarily test *everything*, but
    they help you see some of the problems with the current implementation of the
    other functions in lab8a.py.
    """
    time1 = new_time(new_hour(10), new_minute(15))
    time2 = new_time(new_hour(13), new_minute(30))
    span1 = new_time_span(time1, time2)
    span2 = new_time_span(new_time_from_string("12:10"),
                          new_time_from_string("15:45"))

    assert time_equals(ts_start(span1), time1)
    assert time_equals(ts_end(span1), time2)

    assert ts_equals(span1, span1)
    assert ts_overlap(span1, span2)

    overlap = ts_overlapping_part(span1, span2)

    assert ts_equals(overlap, new_time_span(new_time(new_hour(12), new_minute(10)),
                                            new_time(new_hour(13), new_minute(30))))

    assert duration_equals(ts_duration(overlap), new_duration(new_hour(1), new_minute(20)))
    assert duration_equals(ts_duration(span1), new_duration_from_string("3:15"))
    assert duration_equals(ts_duration(span2), new_duration_from_string("3:35"))

    print("test_timespan_duration: All tests passed.")


if __name__ == '__main__':
    test_ensure_type()
    test_time()
    test_timespan_duration()
