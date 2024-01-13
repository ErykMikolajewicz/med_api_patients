CREATE OR REPLACE FUNCTION patients.get_appointments_list(
	p_patient_id uuid,
	appointments_from date,
	appointments_to date)
    RETURNS table
	(
		"id" uuid,
		patient_id uuid,
		"start" timestamp without time zone,
		"end" timestamp without time zone,
		employee_id uuid
	)
	LANGUAGE 'sql'
AS $BODY$

SELECT
	"id"
	,employee_id
	,"start"
	,"end"
	,patient_id
FROM patients.appointments
WHERE patient_id = patient_id
	and ("start" >= appointments_from or appointments_from is null)
	and ("end" <= appointments_to or appointments_to is null);

$BODY$;