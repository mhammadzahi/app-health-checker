import requests, time, base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
EMAIL_SENT = False



def send_mail(subject):
    try:

        message_text = f"{subject}"

        creds = Credentials.from_authorized_user_file('pt_llc_out.json', SCOPES)
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEMultipart()
        #message['from'] = 'From-Name <name@yourdomain.com>'
        message['to'] = "mohamedzahi33@gmail.com"
        message['subject'] = subject
        message.attach(MIMEText(message_text, 'plain'))

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': raw_message}

        message = service.users().messages().send(userId='me', body=body).execute()
        print(f"Message sent! Message Id: {message['id']}")

    except HttpError as e:
        print(f'An error occurred: {e}')



def send_request(app_url):
    global EMAIL_SENT

    try:
        response = requests.get(app_url)
        response_data = response.json()
        print(response_data)

        if response_data is None:
            if not EMAIL_SENT:
                send_mail(f"{response_data}")
                EMAIL_SENT = True

    except Exception as e:
        if not EMAIL_SENT:
            print(str(e))
            send_mail(f"{e}")
            EMAIL_SENT = True



if __name__ == "__main__":
    while True:
        send_request("")
        time.sleep(150)

