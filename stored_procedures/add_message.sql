CREATE OR REPLACE FUNCTION patients.add_message(
	p_patient_id uuid,
	p_specialist_id uuid,
	p_title text,
	p_message text,
	OUT "id" uuid,
	OUT patient_id uuid,
	OUT specialist_id uuid,
	OUT title character varying,
	OUT message character varying,
	OUT create_date timestamp,
	OUT is_patient_message boolean
)
RETURNS record
LANGUAGE 'sql'

AS $BODY$

INSERT INTO patients.messages
(
	patient_id
	,specialist_id
	,title
	,"message"
	,is_patient_message
)
VALUES
(
	p_patient_id
	,p_specialist_id
	,p_title
	,p_message
	,true
)
RETURNING "id", patient_id, specialist_id, title, "message", create_date, is_patient_message;

$BODY$;