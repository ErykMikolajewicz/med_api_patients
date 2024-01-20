CREATE OR REPLACE FUNCTION patients.add_email_verification(
	p_verification_parameter varchar,
	p_patient_id uuid,
    OUT verification_parameter varchar)
    LANGUAGE 'sql'

AS $BODY$


INSERT INTO patients.verify_email
(
	verification_parameter
	,patient_id
	,verification_time
)
VALUES
(
	p_verification_parameter
	,p_patient_id
	,now() + interval '2' day
)
RETURNING verification_parameter;

$BODY$;