import smtplib

import boto3

from app.config import SES_FROM_EMAIL


def send_email(recipients, subject, body):
    session = boto3.Session()
    client = session.client("ses")
    try:
        client.send_email(
            Source=SES_FROM_EMAIL,
            Destination={
                "ToAddresses": recipients,
            },
            Message={
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": {
                    "Html": {"Data": body, "Charset": "UTF-8"},
                },
            },
            ReplyToAddresses=[
                SES_FROM_EMAIL,
            ],
        )
    except Exception as e:
        print(e)
        return False
    return True
