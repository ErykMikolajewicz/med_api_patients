from uuid import UUID
import os
import json

from src.repositories.patients import EmailVerification, Patients
from src.services.helpers import RandomStringCreator
from src.domain.services.patients import send_email_to_patient
from src.texts.patients import EmailVerification


MED_APP_EMAIL_SECRETS_FILE = os.environ["MED_APP_EMAIL_SECRETS_FILE"]
with open(MED_APP_EMAIL_SECRETS_FILE, 'r') as file:
    med_app_email_secrets = json.load(file)


async def check_patient_email(session, verification_parameter: str) -> UUID | None:
    email_verification_data_access = EmailVerification(session)
    email_verification_result = await email_verification_data_access.get(verification_parameter)
    try:
        patient_id: UUID = email_verification_result['patient_id']
        return patient_id
    except TypeError:
        return None


async def verify_patient_email(session, patient_id: UUID) -> str:
    patients_data_access = Patients(session)
    email = await patients_data_access.verify_email(patient_id)
    return email


async def send_verification_email(patient_id: UUID, email: str, pool):
    string_creator = RandomStringCreator(255)
    verification_parameter = string_creator.create_string()
    async with pool.acquire() as session:
        email_verification_data_access = EmailVerification(session)
        verification_data = await email_verification_data_access.add(verification_parameter, patient_id)

    med_app_email = med_app_email_secrets['email']
    med_app_password = med_app_email_secrets['password']

    subject = EmailVerification.email_subject
    body = EmailVerification.email_body
    body = body.format(verification_parameter=verification_parameter)

    send_email_to_patient(email, med_app_email, med_app_password, subject, body)




