CREATE OR REPLACE FUNCTION patients.get_appointment(
	appointment_id uuid)
    RETURNS TABLE(id uuid, patient_id uuid, start timestamp without time zone, "end" timestamp without time zone, specialist_id uuid)
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
WHERE appointment_id = "id";

$BODY$;

ALTER FUNCTION patients.get_appointment(uuid)
    OWNER TO postgres;