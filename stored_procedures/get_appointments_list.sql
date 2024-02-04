CREATE OR REPLACE FUNCTION patients.get_appointments_list(
	p_patient_id uuid,
	appointments_from date,
	appointments_to date)
    RETURNS TABLE
	(
		"id" uuid,
		patient_id uuid,
		"start" timestamp without time zone,
		"end" timestamp without time zone,
		specialist_id uuid
	)
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$

SELECT
	"id"
	,patient_id
	,"start"
	,"end"
	,specialist_id
FROM patients.appointments
WHERE patient_id = patient_id
	and ("start" >= appointments_from or appointments_from is null)
	and ("end" <= appointments_to or appointments_to is null);

$BODY$;