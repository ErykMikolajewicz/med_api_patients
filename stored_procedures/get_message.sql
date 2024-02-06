CREATE OR REPLACE FUNCTION patients.get_message(message_id uuid)
RETURNS TABLE
(
	"id" uuid
	,patient_id uuid
	,specialist_id uuid
	,title text
	,"message" text
	,create_date timestamp
	,is_patient_message bool
)
LANGUAGE 'sql'

AS $BODY$

SELECT
	 "id"
	 ,patient_id
	 ,specialist_id
	 ,title
	 ,"message"
	 ,create_date
	 ,is_patient_message
FROM patients.messages
WHERE message_id = "id";

$BODY$;