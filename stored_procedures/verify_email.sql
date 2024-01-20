CREATE OR REPLACE FUNCTION patients.verify_email(
	patient_id uuid,
    OUT email varchar)
    LANGUAGE 'sql'

AS $BODY$

UPDATE patients.patients SET
	email_verified = true
WHERE "id" = patient_id
RETURNING email;

$BODY$;