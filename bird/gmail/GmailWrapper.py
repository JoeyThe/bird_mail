import base64
import os
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://mail.google.com/"]


class GmailWrapper:
    def __init__(self):
        TOKEN_PATH = os.path.join(os.path.realpath(__file__).replace(os.path.realpath(__file__).split("/")[-1], ""), "token.json")
        CRED_PATH = os.path.join(os.path.realpath(__file__).replace(os.path.realpath(__file__).split("/")[-1], ""), "credentials.json")
        self.FROM_ADDR = "joseph.girardini@gmail.com"
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(TOKEN_PATH):
            self.creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CRED_PATH, SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(TOKEN_PATH, "w") as token:
                token.write(self.creds.to_json())
            print("Credentials generated, exiting application. Please run again.")
            exit(0)

    def send_gmail_message(self, content: str, to_addr: str, subject: str):
        try:
            service = build("gmail", "v1", credentials=self.creds)
            message = EmailMessage()

            message.set_content(content)

            message["To"] = to_addr
            message["From"] = self.FROM_ADDR
            message["Subject"] = subject

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {"raw": encoded_message}
            # pylint: disable=E1101
            send_message = service.users().messages().send(userId="me", body=create_message).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")
            send_message = None
        return send_message
