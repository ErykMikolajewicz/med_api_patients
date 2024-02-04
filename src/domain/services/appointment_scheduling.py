from datetime import datetime, timedelta


def validate_specialist_working_time(appointment, specialist_working_time) -> bool:
    if specialist_working_time is None or specialist_working_time['is_working_day'] is False:
        return False

    visit_start_time = appointment['start'].time()
    visit_end_time = appointment['end'].time()

    work_start = specialist_working_time['work_start']
    work_end = specialist_working_time['work_end']

    if visit_start_time < work_start or visit_end_time > work_end:
        return False

    work_break_start = specialist_working_time['work_break_start']
    work_break_end = specialist_working_time['work_break_end']

    if work_break_start < visit_start_time < work_break_end:
        return False

    if work_break_start < visit_end_time < work_break_end:
        return False

    return True


def check_can_be_canceled(appointment) -> bool:
    time_to_visit: timedelta = appointment['start'] - datetime.now()
    hours_to_visit = time_to_visit.total_seconds()/60/60
    if hours_to_visit > 12:
        return True
    else:
        return False
