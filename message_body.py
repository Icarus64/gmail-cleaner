from __future__ import print_function
import email


import os.path
import json
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://mail.google.com/",
]


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    message_id = "18938abce7311077"

    try:
        service = build('gmail', 'v1', credentials=creds)

        # Call the Gmail v1 API, retrieve message data.
        message = service.users().messages().get(userId='me', id=message_id, format='raw').execute()

        # Parse the raw message.
        mime_msg = email.message_from_bytes(base64.urlsafe_b64decode(message['raw']))

        print(mime_msg['from'])
        print(mime_msg['to'])
        print(mime_msg['subject'])

        print("----------------------------------------------------")
        # Find full message body
        message_main_type = mime_msg.get_content_maintype()
        if message_main_type == 'multipart':
            for part in mime_msg.get_payload():
                if part.get_content_maintype() == 'text':
                    print(part.get_payload())
        elif message_main_type == 'text':
            print(mime_msg.get_payload())
        print("----------------------------------------------------")

        # Message snippet only.
        # print('Message snippet: %s' % message['snippet'])
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'A message get error occurred: {error}')


if __name__ == "__main__":
    main()
