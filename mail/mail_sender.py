import smtplib
from email.mime.text import MIMEText

from loggin.loggin import config_logger



class MailSender():
    def __init__(self, host="localhost"):
        self.LOGGER = config_logger(handlers=['file_handler', 'console_handler'], host=host)
    def send(self, subject, body, sender, password, recipient):
        self.LOGGER.debug(f'Sending mail to {recipient}')
        if isinstance(body, bytes):
            self.LOGGER.debug('Decoding message')
            body = body.decode('utf-8')

        self.LOGGER.debug('Creating mail')
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipient, msg.as_string())

        self.LOGGER.info(f'Sended message to {recipient}')