# Write your code for lab 8d here.

from test_driver import store_test_case, run_free_spans_tests


# Create additional test cases, and add to them to create_tests_for_free_span().

def create_tests_for_free_span() -> dict:
    """Create and return a number of test cases for the free_spans function"""
    test_cases = dict()

    store_test_case(
        test_cases,
        1,
        start_str="08:00",  # Search interval starts
        end_str="21:00",  # Search interval ends
        booking_data=["07:00-09:00", "13:00-18:00"],  # This day's appointments
        exp_result=["09:00-13:00", "18:00-21:00"],
    )  # Expected free time

    # -------- YOUR TEST CASES GO HERE -----------------------
    # For each case, add a brief description of what you want to test.

    # Tests if a day within the given interval has no appointments.
    store_test_case(
        test_cases,
        2,
        start_str="08:00",  # Search interval starts
        end_str="21:00",  # Search interval ends
        booking_data=[],  # This day's appointments
        exp_result=["08:00-21:00"],
    )  # Expected free time

    # Tests if a day within the given interval is all booked.
    store_test_case(
        test_cases,
        3,
        start_str="08:00",  # Search interval starts
        end_str="21:00",  # Search interval ends
        booking_data=["08:00-21:00"],  # This day's appointments
        exp_result=[], # Eller tom lista?
        #prints: "There are no free spans this day at the given interval"

    )  # Expected free time
    
    # Tests if a day wihtin the given interval has one appointment that starts and ends at a specific minute. 
    store_test_case(
        test_cases,
        4,
        start_str="08:00",  # Search interval starts
        end_str="21:00",  # Search interval ends
        booking_data=["13:03-18:24"],  # This day's appointments
        exp_result=["08:00-13:03", "18:24-21:00"],
    )  # Expected free time
    
    # Tests if a day within the given interval is all booked except for half an hour 
    # (checks if it can return an interval within the same hour).
    store_test_case(
        test_cases,
        5,
        start_str="08:00",  # Search interval starts
        end_str="21:00",  # Search interval ends
        booking_data=["08:00-18:00", "18:30-21:00"],  # This day's appointments
        exp_result=["18:00-18:30"],
    )  # Expected free time

    # Tests if the given interval is empty. (Behövs denna?)
    store_test_case(
        test_cases,
        6,
        start_str="08:00",  # Search interval starts
        end_str="08:00",  # Search interval ends
        booking_data=["13:00-18:00"],  # This day's appointments
        exp_result=[], # Vad borde resultatet bli?
    )  # Expected free time

    # Tests if the given interval is less than an hour. 
    store_test_case(
        test_cases,
        7,
        start_str="08:00",  # Search interval starts
        end_str="08:15",  # Search interval ends
        booking_data=["13:00-18:00"],  # This day's appointments
        exp_result=["08:00-08:15"],
    )  # Expected free time

    # Tests if the given interval is free before an after an appointment.
    store_test_case(
        test_cases,
        8,
        start_str="08:00",  # Search interval starts
        end_str="12:00",  # Search interval ends
        booking_data=["09:00-11:00"],  # This day's appointments
        exp_result=["08:00-09:00", "11:00-12:00"],
    )  # Expected free time
    
    # Tests if one appointment starts where the other ended.
    store_test_case(
        test_cases,
        9,
        start_str="08:00",  # Search interval starts
        end_str="21:00",  # Search interval ends
        booking_data=["13:00-18:00", "18:00-19:00"],  # This day's appointments
        exp_result=["08:00-13:00", "19:00-21:00"],
    )  # Expected free time

    # Tests if there are many appointments within the interval.
    store_test_case(
        test_cases,
        10,
        start_str="08:00",  # Search interval starts
        end_str="21:00",  # Search interval ends
        booking_data=["08:00-09:00", "10:00-11:00", "12:00-14:00", "16:00-18:00", "19:00-21:00"],  # This day's appointments
        exp_result=["09:00-10:00", "11:00-12:00", "14:00-16:00", "18:00-19:00"],
    )  # Expected free time

    # Tests if there are appointments but not within the given interval.
    store_test_case(
        test_cases,
        11,
        start_str="19:00",  # Search interval starts
        end_str="21:00",  # Search interval ends
        booking_data=["13:00-19:00", "21:00-23:00"],  # This day's appointments
        exp_result=["19:00-21:00"],
    )  # Expected free time

    # Tests if there are many appointments within the same hour.
    store_test_case(
        test_cases,
        12,
        start_str="10:00",  # Search interval starts
        end_str="11:00",  # Search interval ends
        booking_data=["10:00-10:05", "10:10-10:20", "10:30-10:45", "10:45-10:55"],  # This day's appointments
        exp_result=["10:05-10:10", "10:20-10:30", "10:55-11:00"],
    )  # Expected free time
    
    print("Test cases generated.")

    return test_cases


if __name__ == '__main__':
    # Actually run the tests, using the test driver functions
    tests = create_tests_for_free_span()
    
    run_free_spans_tests(tests)