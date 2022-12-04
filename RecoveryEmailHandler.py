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
            <header style="font-family:verdana; text-align: center; color: white; background: #198754;
                            padding: 15px 35px;">
                <h2>ComeFundMe Username Recovery</h2> 
            </header>
            <body style="font-family:verdana; background: #eee !important; margin: 0;">
                <br>
                <div style="margin-top: 300px; max-width: 380px; padding: 15px 35px 45px; color: black;
                            margin: auto; background-color: #fff; border: 5px solid rgba(0,0,0,0.1);">
                    <p>
                        Your current username is: %s
                    </p>
                    <p> 
                        If you we not expecting to receive this email, <i>contact support immediately</i> at 573-555-0107.
                    </p>
                </div> <br><br><br>
                <div style="color: black; margin-left: 10px; margin-bottom: 10px;">
                    <p>Come Fund Me</p>
                    <p>Established in 2022</p>
                    <p>5000 Holmes St. Kansas City, MO</p>
                    <p>Not a real fundraising site</p>
                </div>
            </body>
        </html>
        """ % (recovered_data)
    elif (email_type == RecoveryType.PASSWORD):
        body = """
        <html>
            <header style="font-family:verdana; text-align: center; color: white; background: #198754;
                            padding: 15px 35px;">
                <h2>ComeFundMe Password Recovery</h2> 
            </header>
            <body style="font-family:verdana; background: #eee !important; margin: 0;">
                <br>
                <div style="margin-top: 300px; max-width: 380px; padding: 15px 35px 45px; color: black;
                            margin: auto; background-color: #fff; border: 5px solid rgba(0,0,0,0.1);">
                    <p>
                        Click <a href="http://127.0.0.1:5000/new-password">here</a> to reset your password.
                    </p>
                    <p> 
                        If you we not expecting to receive this email, <i>contact support immediately</i> at 573-555-0107.
                    </p>
                </div> <br><br><br>
                <div style="color: black; margin-left: 10px; margin-bottom: 10px;">
                    <p>Come Fund Me</p>
                    <p>Established in 2022</p>
                    <p>5000 Holmes St. Kansas City, MO</p>
                    <p>Not a real fundraising site</p>
                </div>
            </body>
        </html>
        """

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
