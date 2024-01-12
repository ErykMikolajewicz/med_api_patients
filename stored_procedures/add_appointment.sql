CREATE OR REPLACE FUNCTION patients.add_appointment(
	p_employee_id uuid,
	p_start timestamp without time zone,
	p_end timestamp without time zone,
	p_patient_id uuid,
	OUT "id" uuid,
	OUT patient_id uuid,
	OUT "start" timestamp without time zone,
	OUT "end" timestamp without time zone,
	OUT employee_id uuid)
    RETURNS record
    LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
	previous_visit_end timestamp;
	next_visit_start timestamp;
	p_start_with_break timestamp;
	p_end_with_break timestamp;
BEGIN

p_start_with_break := p_start - INTERVAL '5 min';
p_end_with_break := p_end + INTERVAL '5 min';

LOCK TABLE patients.appointments;

previous_visit_end := (SELECT max(appointments.end) FROM patients.appointments
						WHERE appointments.employee_id = p_employee_id and appointments.start < p_start);
next_visit_start := (SELECT min(appointments.start) FROM patients.appointments
					 WHERE appointments.employee_id = p_employee_id and appointments.start > p_start);

IF (p_start_with_break >= previous_visit_end or previous_visit_end is null)
	and (p_end_with_break <= next_visit_start or next_visit_start is null) THEN
	INSERT INTO patients.appointments
	(
		employee_id,
		"start",
		"end",
		patient_id
	)
	VALUES
	(
		p_employee_id,
		p_start,
		p_end,
		p_patient_id
	)
	RETURNING * INTO $5, $6, $7, $8, $9;

ELSE
	RAISE EXCEPTION 'Visit date engaged!';
END IF;

END
$BODY$;