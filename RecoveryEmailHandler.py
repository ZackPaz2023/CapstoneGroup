from email.message import EmailMessage
from enum import Enum
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib


class RecoveryType(Enum):
    USERNAME = 1
    PASSWORD = 2


def construct_email(email_type, recovered_data, receiver):
    email_sender = 'newdeveloper378@gmail.com'
    email_receiver = receiver

    subject = 'noreply'
    body = ""
    if (email_type == RecoveryType.USERNAME):

        body = """
        <html>
            <body style="font-family:verdana; color:black;">
                <h2>Come Fund Me Username Recovery</h2> 
                <p>
                    Your current username is: %s
                </p>
                <p> 
                    If you we not expecting to receive this email, <i>contact support immediately</i> at 573-555-0107.
                </p>
            </body>
            <footer style="font-family:verdana; color:grey;">
                <p>Come Fund Me</p>
                <p>Established in 2022</p>
                <p>Not a real fundraising site</p>
            </footer>
        </html>
        """ % (recovered_data)
    elif (email_type == RecoveryType.PASSWORD):
        body = """
        <html>
            <body style="font-family:verdana; color:black;">
                <h2>Come Fund Me Password Recovery</h2> 
                <p>
                    Your current password is: %s
                </p>
                <p> 
                    If you we not expecting to receive this email, <i>contact support immediately</i> at 573-555-0107.
                </p>
            </body>
            <footer style="font-family:verdana; color:grey;">
                <p>Come Fund Me</p>
                <p>Established in 2022</p>
                <p>Not a real fundraising site</p>
            </footer>
        </html>
        """ % (recovered_data)

    em = MIMEMultipart("alternative")
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject

    em_part1 = MIMEText(body, "html")
    em.attach(em_part1)

    return em


def send_email(email_type, recovered_data, receiver):
    email_sender = 'newdeveloper378@gmail.com'
    email_password = 'rmlr zjba wmwj mqbd'
    email_receiver = receiver
    em = construct_email(email_type, recovered_data, receiver)

    ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
