CREATE OR REPLACE FUNCTION patients.add_patient(
	p_telephone character varying,
	p_email character varying,
	p_address character varying,
	p_login character varying,
	p_name character varying,
	p_surname character varying,
	p_sex character varying,
	p_pesel_or_identifier character varying,
	p_birth_date date,
	p_hashed_password bytea)
    RETURNS RECORD
    LANGUAGE 'sql'
AS $BODY$
INSERT INTO patients.patients
(
	telephone,
	email,
	address,
	login,
	"name",
	surname,
	sex,
	pesel_or_identifier,
	birth_date,
	hashed_password
)
VALUES
(
	p_telephone,
	p_email,
	p_address,
	p_login,
	p_name,
	p_surname,
	p_sex,
	p_pesel_or_identifier,
	p_birth_date,
	p_hashed_password
)
RETURNING
	"id"
	,login
	,"name"
	,surname
	,sex
	,pesel_or_identifier
	,birth_date
	,telephone
	,email
	,address;
$BODY$;