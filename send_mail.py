#!/usr/bin/env python3

import smtplib
import argparse
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver_email, subject, body):
    # Hardcoded SMTP server details and sender credentials
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender_email = os.environ["SRC_MAIL"]
    password = os.environ["SRC_PASS"]  # Assuming the password is set as an environment variable

    # Create a MIMEText object to represent the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the body to the email
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Send an email using runtime arguments.')
    parser.add_argument('--receiver_email', type=str, required=True, help='Receiver email address')
    parser.add_argument('--subject', type=str, required=True, help='Email subject')
    parser.add_argument('--body', type=str, required=True, help='Email body')

    # Parse arguments
    args = parser.parse_args()

    # Send the email
    send_email(args.receiver_email, args.subject, args.body)

if __name__ == '__main__':
    main()