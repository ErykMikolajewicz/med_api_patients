from email.mime.text import MIMEText
import smtplib


def send_email_to_patient(patient_email, med_app_email, password, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = med_app_email
    msg['To'] = patient_email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(med_app_email, password)
        smtp_server.sendmail(med_app_email, patient_email, msg.as_string())
