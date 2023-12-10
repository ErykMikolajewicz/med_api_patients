CREATE PROCEDURE patients.add_patient(
    IN p_telephone varchar,
    IN p_email varchar,
    IN p_address varchar,
    IN p_login varchar,
    IN p_name varchar,
    IN p_surname varchar,
    IN p_sex varchar,
    IN p_pesel_or_identifier varchar,
    IN p_birth_date date,
    IN p_hashed_password bytea
)
LANGUAGE sql
AS &BODY&
BEGIN

INSERT INTO patients.patients
(
telephone,
email,
address,
login,
name,
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
RETURNING * as result;

SELECT result;

END;
$Body$