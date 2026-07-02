import smtplib
from email.message import EmailMessage

EMAIL_USER = "barath.t2024@vitstudent.ac.in"
EMAIL_PASS = "aazfkjpfqknjgzfy"
TO_EMAIL = "contactmebarath@gmail.com"

msg = EmailMessage()
msg["Subject"] = "Test Email"
msg["From"] = EMAIL_USER
msg["To"] = TO_EMAIL
msg.set_content("This is a test email from Python.")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_USER, EMAIL_PASS)
    smtp.send_message(msg)

print("Email sent")