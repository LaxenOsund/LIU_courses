#from cal_abstraction import *
from cal_output import *
from cal_abstraction import *
# =========================================================================
# Type definition
# =========================================================================

# Define the type somehow...  The initial "" is simply here as a placeholder.
TimeSpanSeq =  NamedTuple(
    "TimeSpanSeq", [("timespans", List[TimeSpan])]
)



# =========================================================================
#  Function implementations
# =========================================================================

# Implement these functions!  Also determine if you need *additional* functions.

def new_time_span_seq(seq: List[TimeSpan] = None) -> TimeSpanSeq:
    """
    Creates a new time span sequence. If no timespan are given then
    return a timespan sequence with an empty sequence
    """
    if seq == None:
        seq = []
    else:
        ensure_type(seq, List[TimeSpan])
    
    return TimeSpanSeq(seq)

    
def tss_is_empty(tss: TimeSpanSeq) -> bool:
    """return true if timespanseq is empty"""
    ensure_type(tss, TimeSpanSeq)
    return not tss.spans


def tss_plus_span(tss: TimeSpanSeq, ts: TimeSpan) -> TimeSpanSeq:
    """
    Returns a copy of the given TimeSpanSeq, where the given TimeSpan
    has been added in its proper position.
    """
    ensure_type(tss, TimeSpanSeq)
    ensure_type(ts, TimeSpan)

    def add_timespan(ts: TimeSpan, tss: List[TimeSpan]):
        if not tss or time_precedes(ts_start(ts), ts_start(tss[0])):
            return [ts] + tss
        else:
            return [tss[0]] + add_timespan(ts, tss[1:])

    return new_time_span_seq(add_timespan(ts, tss.timespans))


def tss_iter_spans(tss):
    """iterates over a timespan sequence"""
    ensure_type(tss, TimeSpanSeq)
    for timespan in tss.timespans:
        yield timespan


def show_time_spans(tss):
    """shows all the timespans in a timespan sequence"""
    ensure_type(tss, TimeSpanSeq)
    for timespan in tss_iter_spans(tss):
        print()
        show_ts(timespan)
        print()
    print()
        
    


# Keep only time spans that satisfy pred.
# You do not need to modify this function.
def tss_keep_spans(tss, pred):
    result = new_time_span_seq()
    for span in tss_iter_spans(tss):
        if pred(span):
            result = tss_plus_span(result, span)

    return result



time1 = new_time_from_string("12:00")
time2 = new_time_from_string("12:30")

time3 = new_time_from_string("12:00")
time4 = new_time_from_string("13:30")

ts1 = new_time_span(time1, time2)
ts2 = new_time_span(time3,time4)

tss1 = new_time_span_seq()
tss = (tss_plus_span(tss1, ts2))
tss2 = tss_plus_span(tss, ts1)

show_time_spans(tss2)
