CREATE OR REPLACE FUNCTION patients.delete_appointment(appointment_id uuid)
	RETURNS void
    LANGUAGE 'sql'
AS $BODY$

DELETE FROM patients.appointments
WHERE appointment_id = "id";

$BODY$;