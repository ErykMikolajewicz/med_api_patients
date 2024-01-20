from uuid import UUID

from src.repositories.patients import EmailVerification, Patients


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




