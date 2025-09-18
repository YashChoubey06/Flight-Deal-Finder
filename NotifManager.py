import os
from twilio.rest import Client
import smtplib

class NM:

    def __init__(self):
        self.client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ["TWILIO_AUTH_TOKEN"])

    def send_sms(self, message_body):

        message = self.client.messages.create(
            from_=os.environ["TWILIO_VIRTUAL_NUMBER"],
            body=message_body,
            to=os.environ["TWILIO_PERSONAL_NUMBER"]
        )

        print(f"Your message is {message.status}")

    def send_mails(self, mail_list,body):

        my_email = os.getenv("MYMAIL")
        my_pass = os.getenv("MYPASS")
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:

            connection.starttls()
            connection.login(
                user=my_email,
                password=my_pass
            )

            for reciever_mail in mail_list:
                connection.sendmail(
                    from_addr=my_email,
                    msg=f"Subject:Hello Dear Subscriber!!\n\n{body}",
                    to_addrs=reciever_mail
                )
