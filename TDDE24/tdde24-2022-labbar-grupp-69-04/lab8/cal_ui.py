# =========================================================================
#  The Calendar - Functional and imperative programming in Python
#
#  Module: cal_ui.py
#  Updated: 2004-11-10 by Peter Dalenius
#    Translated to Python in 2012 by Peter L-G
#    Translated to English in 2013 by Anders M.L.
#    Changes in 2020 by Jonas K (NamedTuple, type hints, ...)
#  Dependencies:
#    cal_abstraction.py
#    cal_booking.py
#    cal_output.py
# =========================================================================

# This module ties the calendar together. It contains the functions
# that users interact with, and the global dictionary where all
# calendars are stored.

# Functions in this file never delve deeper into the representation of the
# calendar objects, or the internal logic of actually booking an appointment.
# Such code is available in separate modules. These are imported automatically
# upon the import of the calendar module.

# The files have the following dependencies:

#
#               cal_ui.py
#                   |
#           +_______+________+
#           |                |
#      cal_booking.py   cal_output.py
#           |                |
#           +_______+________+
#                   |
#              cal_abstraction.py

from cal_booking import *
from cal_output import *

import pickle

# =========================================================================
#  1. Storing and fetching calendars
# =========================================================================

# Right now a CalendarSet is a plain dict.
CalendarSet = dict

# Global variables are not nice... but in this case we are using the Python
# prompt as the user interface, so we don't have a continuously running
# program that can store the calendars somewhere non-global.
calendars = CalendarSet()


def get_calendar(cal_name: str) -> CalendarYear:
    """Retrieve the calendar (year) with the given name.
    The calendar must already exist."""
    if calendar_exists(cal_name):
        return calendars[cal_name]
    else:
        message = f"There is no calendar by the name {cal_name}."
        raise ValueError(message)


def insert_calendar(cal_name: str, cal_year: CalendarYear) -> None:
    """Store the given calendar (year) under the given name."""
    ensure_type(cal_name, str)
    ensure_type(cal_year, CalendarYear)
    calendars[cal_name] = cal_year


def calendar_exists(cal_name: str) -> bool:
    """Return true iff there exists a calendar with the given name."""
    ensure_type(cal_name, str)
    return cal_name in calendars


def new_calendar(cal_name: str) -> None:
    """
    Create a new calendar (year) with the given name, without checking
    if such a calendar already exists.
    """
    ensure_type(cal_name, str)
    calendars[cal_name] = new_calendar_year()


def save_calendars(filename: str) -> None:
    """
    Saves all calendars to file. The data is wrapped in [*CALFILE3000*, ...]
    which is used as a tag for identifying calendar files.
    """
    with open(filename, "wb") as output:
        pickle.dump(["*CALFILE3000*", calendars], output)


def load_calendars(filename: str) -> bool:
    """
    Loads a set of calendars from the file with the given name.

    If the file does not exist, cannot be read, or cannot be unpickled,
    an exception is raised.

    If the file can be read and contains correctly pickled data, but does not
    have the proper high level structure, False is returned.

    Otherwise, True is returned.

    The file to be loaded is assumed to be non-hostile (cf the warning in the
    Pickle module documentation http://docs.python.org/3/library/pickle.html).
    """
    with open(filename, "rb") as pkl_file:
        content = pickle.load(pkl_file)

    if (
        isinstance(content, list)
        and len(content) == 2
        and content[0] == "*CALFILE3000*"
    ):
        global calendars
        calendars = content[1]
        return True
    else:
        return False


# =========================================================================
#  2. User interface
# =========================================================================


def create(cal_name: str) -> None:
    """
    Create a calendar (year) with the given name.  The calendar must not
    already exist.
    """
    ensure_type(cal_name, str)
    if calendar_exists(cal_name):
        print(f"A calendar by the name {cal_name} already exists.")
    else:
        new_calendar(cal_name)
        print(f"A new calendar by the name {cal_name} has been created.")


def show_calendars() -> None:
    """Show the names of all calendars that have been created."""
    if calendars:
        print("The following calendars exist:")
        for cal_name in calendars:
            print(cal_name)
    else:
        print("No calendars have been created.")


def book(cal_name: str, d: int, m: str, t1: str, t2: str, subject_txt: str) -> None:
    """Book a new appointment in the calendar with the given name."""
    day = new_day(d)
    mon = new_month(m)
    start = new_time_from_string(t1)
    end = new_time_from_string(t2)
    subject = new_subject(subject_txt)
    cal_year = get_calendar(cal_name)
    cal_month = cy_get_month(mon, cal_year)
    cal_day = cm_get_day(cal_month, day)

    # Ensure that the date is proper.  If not, this will raise an exception.
    new_date(day, mon)

    if time_precedes(end, start):
        print("Invalid appointment time (wrong order of start and finish).")
    elif is_booked_during(cal_day, new_time_span(start, end)):
        print("The proposed time is already taken.")
    else:
        # Get a new CalendarYear with the new appointment...
        new_year = plus_appointment(cal_year, day, mon, start, end, subject)
        # ...and let the calendar name refer to this CalendarYear instead.
        insert_calendar(cal_name, new_year)
        print("The appointment has been booked.")


def show(cal_name: str, d: int, m: str) -> None:
    """Show all appointments in the calendar with the given name,
    during the given date (day and month)."""
    day = new_day(d)
    mon = new_month(m)
    cal_day = cm_get_day(cy_get_month(mon, get_calendar(cal_name)), day)

    new_date(day, mon)  # Ensure that the date is proper

    if cd_is_empty(cal_day):
        print("No appointments this day.\n")
    else:
        show_day_heading(day, mon)
        show_cd(cal_day)


def save(filename: str) -> None:
    """Save the current set of calendars to the file with the given name."""
    save_calendars(filename)
    print(f"The calendars have been saved to {filename}.")


def load(filename: str) -> None:
    """Load a set of calendars from the file with the given name."""
    try:
        if load_calendars(filename):
            print("New calendars have been loaded.")
        else:
            print("The file does not exist, or it is devoid of saved calendars.")
    except IOError as e:
        print(f"Error opening or reading calendar file {filename}")
        print(e)


def calhelp() -> None:
    """Show help for the calendar system."""
    print("The Calendar. \n\n")
    print("-" * 50)
    print("A quick reminder of your options:")
    print("  create(name)")
    print("  book(name, day, month, start, end, subject)")
    print("  show(name, day, month)")
    print("  save(filename)")
    print("  load(filename)")
