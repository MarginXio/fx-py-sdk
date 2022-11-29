import os
import logging

def send_mail(subject, text, recipients=None, attachments=[]):
    try:
        from gmail import GMail, Message

        sender = os.environ['GMAIL_APP_EMAIL']
        password = os.environ['GMAIL_APP_PASSWORD']

        if not recipients:
            recipients = sender

        gmail = GMail(f'FX Dex Database Alerts <{sender}>', password)
        msg = Message(subject, to=recipients or sender, text=text, attachments=attachments)
        gmail.send(msg)
    except Exception as ex:
        logging.error(f'Failed to send e-mail {ex}')
