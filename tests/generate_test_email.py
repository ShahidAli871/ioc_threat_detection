from email.message import EmailMessage
from pathlib import Path

OUT = Path(__file__).parent / "sample_emails" / "sample.eml"

msg = EmailMessage()
msg["From"] = "attacker@example.com"
msg["To"] = "victim@example.com"
msg["Subject"] = "Urgent: verify your account"
msg.set_content("Please login at https://bad.example.com/login and enter your password.")

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "wb") as f:
    f.write(bytes(msg))

print("Sample email written to:", OUT)
