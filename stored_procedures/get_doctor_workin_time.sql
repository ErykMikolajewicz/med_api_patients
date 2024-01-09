CREATE OR REPLACE FUNCTION patients.get_doctor_working_time(
	p_doctor_id uuid,
	p_visit_date date,
	OUT day_of_week_id int,
	OUT accepted_visit_duration int[],
	OUT work_start time,
	OUT work_end time,
	OUT work_break_start time,
	OUT work_break_end time,
	OUT is_working_day bool,
	OUT individual_break_start timestamp,
	OUT individual_break_end timestamp)
    RETURNS record
    LANGUAGE 'sql'
AS $BODY$
SELECT
	t1.day_of_week_id
	,t1.accepted_visit_duration
	,t1.work_start
	,t1.work_end
	,t1.work_break_start
	,t1.work_break_end
	,t1.is_working_day
	,t2.work_break_start as individual_break_start
	,t2.work_break_end as individual_break_end
FROM doctors_working_time as t1
	LEFT JOIN individual_working_breaks as t2 ON t1.doctor_id = t2.doctor_id
	and t2.work_break_start::date = p_visit_date
WHERE t1.doctor_id = p_doctor_id
	and day_of_week_id = extract(isodow from p_visit_date);
$BODY$;