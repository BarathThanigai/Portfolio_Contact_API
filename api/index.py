from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import smtplib
import os
from email.message import EmailMessage

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://barath-portfolio-psi.vercel.app/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")


class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str


@app.get("/")
def home():
    return {"message": "Contact API is running on Vercel"}


@app.post("/contact")
def contact(form: ContactForm):
    try:
        msg = EmailMessage()
        msg["Subject"] = f"Portfolio | New Contact Message from {form.name}"
        msg["From"] = f"Barath Portfolio <{EMAIL_USER}>"
        msg["To"] = TO_EMAIL
        msg["Reply-To"] = form.email

        msg.set_content(
            f"""
New Portfolio Contact

Name: {form.name}
Email: {form.email}

Message:
{form.message}
"""
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)

        return {"success": True, "message": "Email sent successfully"}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to send email")