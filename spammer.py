import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email)

def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def send_emails(to_address, from_address, message, count, smtp_server, smtp_port, login, password):
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as smtpserver:
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(login, password)
            for i in range(count):
                msg = MIMEMultipart()
                msg['From'] = from_address
                msg['To'] = to_address
                msg['Subject'] = 'Notification'
                msg.attach(MIMEText(message, 'plain'))
                smtpserver.sendmail(from_address, to_address, msg.as_string())
                logging.info(f'Email {i + 1} sent successfully.')
        logging.info('All emails sent successfully!')
    except Exception as e:
        logging.error(f'Failed to send email: {e}')

def main():
    config = load_config('config.ini')
    to_address = input("Enter recipient's email:\n")
    from_address = input("Enter your email:\n")
    message = input("Enter your message:\n")
    count = int(input("Number of emails:\n"))
    if not validate_email(to_address) or not validate_email(from_address):
        logging.error("Invalid email format.")
        return
    smtp_server = config['SMTP']['Server']
    smtp_port = int(config['SMTP']['Port'])
    login = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASSWORD')
    if not login or not password:
        logging.error("Email user or password environment variables are not set.")
        return
    send_emails(to_address, from_address, message, count, smtp_server, smtp_port, login, password)

if __name__ == '__main__':
    main()
