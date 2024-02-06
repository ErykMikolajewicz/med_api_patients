CREATE OR REPLACE FUNCTION patients.count_messages(
	p_patient_id uuid,
	p_specialist_id uuid,
	messages_from date,
	messages_to date,
	OUT messages_number bigint
)
RETURNS bigint
LANGUAGE 'sql'
AS $BODY$

SELECT
	COUNT(*) as messages_number
FROM patients.messages
WHERE patient_id = p_patient_id
	and (p_specialist_id = specialist_id or p_specialist_id is null)
	and (create_date >= messages_from or messages_from is null)
	and (create_date <= messages_to or messages_to is null);

$BODY$;