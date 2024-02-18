from email.mime.text import MIMEText

import aiosmtplib


async def send_email_to_patient(patient_email, med_app_email, password, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = med_app_email
    msg['To'] = patient_email
    async with aiosmtplib.SMTP(hostname='smtp.gmail.com', port=465) as email_connection:
        await email_connection.login(med_app_email, password)
        await email_connection.sendmail(med_app_email, patient_email, msg.as_string())
