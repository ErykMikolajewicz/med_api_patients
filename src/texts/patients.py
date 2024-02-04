from dataclasses import dataclass


@dataclass
class EmailVerificationText:
    email_subject: str = 'Please verify your email'
    email_body: str = """
    Thank you for register in MedApp! To verify your account please click link in the down:
    
    http://medapp/verify_email/{verification_parameter}
    
    If you haven't register account in MedApp please ignore this message.
    
    Best regards,
    MedApp team
    """