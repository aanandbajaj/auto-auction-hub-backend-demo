from flask import Blueprint
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

contact_bp = Blueprint('contact',__name__)

def send_email(subject,message,to_email):
    from_email = os.environ