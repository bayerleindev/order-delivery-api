import requests


def send_email(text: str, subject: str):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox407d1d6bfcf044eeaccccf81ada967fa.mailgun.org/messages",
        auth=("api", "280e81e2fd149cbe53e09fd0b12900ab-7a3af442-6bb94cce"),
        data={
            "from": "Excited User <mailgun@sandbox407d1d6bfcf044eeaccccf81ada967fa.mailgun.org>",
            "to": ["giovanni.bayerlein.dev@gmail.com"],
            "subject": subject,
            "text": text,
        },
    )
