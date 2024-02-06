CREATE OR REPLACE FUNCTION patients.get_messages_list(
	p_patient_id uuid,
	p_specialist_id uuid,
	messages_from date,
	messages_to date
)
RETURNS TABLE
(
	id uuid
	, patient_id uuid
	, specialist_id uuid
	, title text
	, create_date timestamp
	,is_patient_message bool
)
LANGUAGE 'sql'

AS $BODY$

SELECT
	 "id"
	 ,patient_id
	 ,specialist_id
	 ,title
	 ,create_date
	 ,is_patient_message
FROM patients.messages
WHERE p_patient_id = patient_id
	and (p_specialist_id = specialist_id or p_specialist_id is null)
	and (messages_from <= create_date or messages_from is null)
	and (messages_to >= create_date or messages_to is null);

$BODY$;