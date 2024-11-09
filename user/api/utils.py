from django.core.mail import EmailMessage

import threading

# Threaded email sending for better performance
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        # Sending the email asynchronously
        self.email.send()

# Utility class for sending emails
class Util:
    @staticmethod
    # Prepare the email message
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.content_subtype = "html"
        # Send the email in a separate thread
        EmailThread(email).start()