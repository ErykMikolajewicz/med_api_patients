CREATE OR REPLACE FUNCTION patients.count_appointments(
	p_patient_id uuid,
	appointments_from date,
	appointments_to date,
	OUT appointments_number bigint)
    LANGUAGE 'sql'
AS $BODY$

SELECT
	COUNT(*) as appointments_number
FROM patients.appointments
WHERE patient_id = p_patient_id
	and ("start" >= appointments_from or appointments_from is null)
	and ("end" <= appointments_to or appointments_to is null);

$BODY$;