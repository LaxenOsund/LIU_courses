from cal_abstraction import *
from cal_booking import *
from cal_ui import *


def remove(cal_name: str, d: int, m: str, t1: str):
    """Ändrar typerna på inputsen till rätt datatyper
    returnerar sedan exec_remove"""
    ensure_type(cal_name, str)
    ensure_type(d, int)
    ensure_type(m, str)
    ensure_type(t1, str)


    d = new_day(d)
    m = new_month(m)
    t1 = new_time_from_string(t1)

    year = get_calendar(cal_name)
    month = cy_get_month(m ,year)
    day = cm_get_day(month, d)
    return exec_remove(cal_name, day, t1, d, m)

#   
def exec_remove(cal_name, day, t1, d, m):
    """kollar iterativt genom alla apointments på en given dag
        appendar sedan dem tiderna som inte är t1. skapar sedan
        ett nytt calender object som i sin tur returneras med
        bokningarna som finns kvar  """
    seq = []
    if is_booked_from(day, t1):
        for appointment in cd_iter_appointments(day):
            timespan = app_span(appointment)
            start_time = ts_start(timespan)
            if not start_time == t1:
                seq.append(appointment)

        new_day = new_calendar_day(d, seq)
        new_month = new_calendar_month(m , [new_day])
        new_year = new_calendar_year([new_month])

        insert_calendar(cal_name, new_year)
        return new_year

create("Felix")
book("Felix", 20, "sep", "12:00", "14:00", "Laga mat")
book("Felix", 20, "sep", "15:00", "16:00", "Redovisa Lab8")
remove("Felix", 20, "sep", "15:00")
book("Felix", 21, "mar", "10:15", "17:00", "Redovisa Lab8 på riktigt")
show("Felix", 20, "sep")
show("Felix", 21, "mar")
