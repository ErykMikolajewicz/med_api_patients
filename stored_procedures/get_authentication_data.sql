CREATE OR REPLACE FUNCTION patients.get_authentication_data(
	p_login character varying,
	OUT "id" uuid,
	OUT hashed_password bytea)
    LANGUAGE 'sql'
AS $BODY$
SELECT
	"id"
	,hashed_password
FROM patients.patients
WHERE login = p_login;
$BODY$;