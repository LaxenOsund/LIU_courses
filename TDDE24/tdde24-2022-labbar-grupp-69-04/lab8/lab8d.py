# Write your code for lab 8d here.
from cal_abstraction import CalendarDay, Time
from cal_ui import *
from settings import CHECK_AGAINST_FACIT

if CHECK_AGAINST_FACIT:
    try:
        from facit_la8_uppg import TimeSpanSeq
    except:
        print("*" * 100)
        print("*" * 100)
        print("Kan inte hitta facit; ändra CHECK_AGAINST_FACIT i test_driver.py till False")
        print("*" * 100)
        print("*" * 100)
        raise
else:
    from lab8b import *


def free_spans(cal_day: CalendarDay, start: Time, end: Time) -> TimeSpanSeq:
    """ Returnerar timespanseq med endast lediga spans """
    #kontrollerar datatyper
    ensure_type(cal_day, CalendarDay)
    ensure_type(start, Time)
    ensure_type(end, Time)
    #definerar inre funktion som räknar ut när på dagen det är ledigt
    def calc_span(appointments: List[Appointment], start, end):
        #kollar om appointments är lediga eller om start == End
        if not appointments or start == end:
            return []
        #hittar första apps start och sluttid samt sätter free_end till sluttiden på spannet
        app_start = ts_start(app_span(appointments[0]))
        app_end = ts_end(app_span(appointments[0]))
        free_end = end
        #kollar om app_start börjar senare än start
        #kollar om slutet och start är samma om dem inte är det 
        #sätts den senare tiden till start
        #kollar om end är samma eller senare än start isåfall returnera
        #en tom lista då det inte finns nån ledig tid.
        if time_precedes_or_equals(app_start, start):
            if not time_equals(app_end, start):
                start = time_latest(app_end, start)
                if time_precedes_or_equals(free_end, start):
                    return []
            #kollar om det finns fler appointments och kallar på sig självt rekursivt om det är så
            #kollar från slut tiden på föregående app och använder free_end som ny end
            #finns det ej returneras ett tidsspan mellan slutet på nuvaranda app och början på nästa

            if appointments[1:]:
                if time_equals(ts_start(app_span(appointments[1])), start):
                    return calc_span(appointments[1:], ts_end(app_span(appointments[1])), free_end)
                else:
                    end = ts_start(app_span(appointments[1]))
            return [new_time_span(start, end)] + calc_span(appointments[1:], end, free_end)
        #om starten på första app inte är samma eller ligger efter start tiden
        else:
            #om free_end inte är senare än första app sätter vi end till app_start
            #returnerar sedan start värdet och slutvärdet + ett rekursivt ropp till sig själv
            #för att kolla vidare.
            if not time_precedes(free_end, app_start):
                end = app_start
            return [new_time_span(start, end)] + calc_span(appointments, end, free_end)
    #kollar om dagen inte har några möten returnerar hela tidsspannet isåfall
    #annars skapas en ny timespan av calc_span
    if cd_is_empty(cal_day):
        return new_time_span_seq([new_time_span(start, end)])
    else:
        return new_time_span_seq(calc_span(cal_day.appointments, start, end))

def show_free(name: str, day: int, month: str, span_start: str, span_end: str):
    """ 
    Skriver ut vilka tidsperioder som är lediga 
    i en almanacka under ett visst intervall en dag. 
    """
    day = new_day(day)
    month = new_month(month)
    span_start = new_time_from_string(span_start)
    span_end = new_time_from_string(span_end)
    cal_year = get_calendar(name)
    cal_month = cy_get_month(month, cal_year)
    cal_day = cm_get_day(cal_month, day)

    # Ensure that the date is proper.  If not, this will raise an exception.
    new_date(day, month)

    free_time = free_spans(cal_day, span_start, span_end)
    show_time_spans(free_time)