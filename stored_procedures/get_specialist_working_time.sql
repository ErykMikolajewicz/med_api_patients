CREATE OR REPLACE FUNCTION patients.get_specialist_working_time(
	p_specialist_id uuid,
	p_visit_date date,
	OUT day_of_week_id integer,
	OUT accepted_visit_duration integer[],
	OUT work_start time without time zone,
	OUT work_end time without time zone,
	OUT work_break_start time without time zone,
	OUT work_break_end time without time zone,
	OUT is_working_day boolean,
	OUT individual_break_start timestamp without time zone,
	OUT individual_break_end timestamp without time zone)
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
FROM specialists_working_time as t1
	LEFT JOIN individual_working_breaks as t2 ON t1.specialist_id = t2.specialist_id
	and t2.work_break_start::date = p_visit_date
WHERE t1.specialist_id = p_specialist_id
	and day_of_week_id = extract(isodow from p_visit_date);

$BODY$;