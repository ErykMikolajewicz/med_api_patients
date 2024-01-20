CREATE OR REPLACE FUNCTION patients.check_email_verification(
	p_verification_parameter varchar)
    RETURNS TABLE
	(
		verification_parameter varchar,
		patient_id uuid
	)
    LANGUAGE 'sql'

AS $BODY$

SELECT
	verification_parameter
	,patient_id
FROM patients.verify_email
WHERE verification_parameter = p_verification_parameter
	and now() < verification_time;

$BODY$;