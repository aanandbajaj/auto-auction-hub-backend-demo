from flask import Blueprint, request, jsonify
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv


contact_form_bp = Blueprint('contact_form',__name__)
load_dotenv()

@contact_form_bp.route('/api/send_email',methods=['POST'])
def send_email():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    user_message = data.get('message')

    sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

    # Create a Mail object
    message = Mail(
        from_email=email,
        to_emails='aanand222@gmail.com',
        subject='Contact Form Submission',
        plain_text_content=user_message
    )

    # Send the email
    try:
        resp = sg.send(message)
        response = jsonify({'message':'Contact form submitted successfully.'})
    except Exception as e:
        response = jsonify({'Error sending email:',str(e)})

    return response





