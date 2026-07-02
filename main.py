from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import smtplib
import os
from email.message import EmailMessage

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-portfolio-link.com"
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
    return {"message": "Contact API is running"}


@app.post("/contact")
def contact(form: ContactForm):
    try:
        msg = EmailMessage()
        msg["Subject"] = f"Portfolio Contact from {form.name}"
        msg["From"] = EMAIL_USER
        msg["To"] = TO_EMAIL
        msg["Reply-To"] = form.email

        msg.set_content(
            f"""
New portfolio message:

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