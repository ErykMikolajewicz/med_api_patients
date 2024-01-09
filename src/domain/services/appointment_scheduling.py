

async def validate_doctors_working_hour(appointment, doctor_working_time):
    if doctor_working_time is None or doctor_working_time['is_working_day'] is False:
        return False

    visit_start_time = appointment['start'].time()
    visit_end_time = appointment['end'].time()

    work_start = doctor_working_time['work_start']
    work_end = doctor_working_time['work_end']

    if visit_start_time < work_start or visit_end_time > work_end:
        return False

    work_break_start = doctor_working_time['work_break_start']
    work_break_end = doctor_working_time['work_break_end']

    if work_break_start < visit_start_time < work_break_end:
        return False

    if work_break_start < visit_end_time < work_break_end:
        return False

    return True


async def validate_visit_accessibility():
    raise NotImplementedError
