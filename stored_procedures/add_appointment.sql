CREATE OR REPLACE FUNCTION patients.add_appointment(
	p_patient_id uuid,
	p_start timestamp without time zone,
	p_end timestamp without time zone,
	p_employee_id uuid,
	OUT p_patient_id uuid,
	OUT p_start timestamp without time zone,
	OUT p_end timestamp without time zone,
	OUT p_employee_id uuid)
    RETURNS record
    LANGUAGE 'sql'
AS $BODY$

INSERT INTO patients.appointments
(
	patient_id,
	"start",
	"end",
	employee_id
)
VALUES
(
	p_patient_id,
	p_start,
	p_end,
	p_employee_id
)
RETURNING
	patient_id,
	"start",
	"end",
	employee_id;
$BODY$;