CREATE OR REPLACE FUNCTION patients.get_specialists_list(
	p_specialist_role_id int)
    RETURNS TABLE
	(
		"id" uuid
		,role_id int
		,"name" varchar
		,surname varchar
		,email varchar
	)
    LANGUAGE 'sql'
AS $BODY$

SELECT
	t1.id
	,t1.role_id
	,t2.name
	,t2.surname
	,t2.email
FROM patients_specialists as t1
	LEFT JOIN employees as t2 ON t1.id = t2.id
WHERE p_specialist_role_id = t1.role_id or p_specialist_role_id is null;

$BODY$;