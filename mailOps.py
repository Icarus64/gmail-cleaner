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

from tokenizer import tokenUpdate


def headerExtract(message_id):
    creds = tokenUpdate()
    try:
        service = build("gmail", "v1", credentials=creds)

        # Call the Gmail v1 API, retrieve message data.
        message = (
            service.users()
            .messages()
            .get(userId="me", id=message_id, format="raw")
            .execute()
        )
        
        # Parse the raw message.
        mime_msg = email.message_from_bytes(base64.urlsafe_b64decode(message["raw"]))

        return {'encoded': message, 'decoded': mime_msg}
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        return f"A message error occurred: {error}"


def idFetcher():
    creds = tokenUpdate()
    try:
        service = build("gmail", "v1", credentials=creds)

        # Call the Gmail v1 API, retrieve message data.
        message_list = service.users().messages().list(userId="me").execute()
        # Parse the raw message.
        return message_list

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"A message get error occurred: {error}")
    return []

def idFetcherAll(nextToken = None):
    creds = tokenUpdate()
    message_list = []
    try:
        service = build("gmail", "v1", credentials=creds)

        # Call the Gmail v1 API, retrieve message data.
        page = service.users().messages().list(userId="me", pageToken = nextToken).execute()
        message_list.append(page)
        while 'nextPageToken' in page and page['nextPageToken']:
            page = service.users().messages().list(userId="me", pageToken = page['nextPageToken']).execute()
            if page != None:
                message_list.append(page)
        return message_list
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"A message get error occurred: {error}")
    
    return None

msg_list = idFetcherAll()
print(len(msg_list))
#msg = headerExtract('18995f9d12fd2585')
#print(msg['decoded'].keys())

