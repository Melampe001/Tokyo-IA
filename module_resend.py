from core_db import log_event
def send_business_email(subj, body):
    print(f"   📧 [RESEND] {subj}")
    log_event("RESEND", subj, "SENT")