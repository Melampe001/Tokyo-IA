from core_db import log_event
def send_alert(title, msg):
    print(f"   🔔 [DISCORD] {title}: {msg}")
    log_event("DISCORD", msg, "SENT")