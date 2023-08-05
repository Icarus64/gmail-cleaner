import email
import base64
import webbrowser
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

        return {"encoded": message, "decoded": mime_msg}
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        return f"A message error occurred: {error}"


def idFetcher():
    creds = tokenUpdate()
    try:
        service = build("gmail", "v1", credentials=creds)

        # Call the Gmail v1 API, retrieve message data.
        message_list = service.users().messages().list(userId="me").execute()
        return message_list

    except HttpError as error:
        print(f"A message get error occurred: {error}")
    return []


def idFetcherAll(nextToken=None):
    creds = tokenUpdate()
    message_list = []
    try:
        service = build("gmail", "v1", credentials=creds)

        # Call the Gmail v1 API, retrieve message data.
        page = (
            service.users().messages().list(userId="me", pageToken=nextToken).execute()
        )
        message_list.append(page)
        if "nextPageToken" in page and page["nextPageToken"]:
            new_page = idFetcherAll(nextToken=page["nextPageToken"])
            if new_page != None:
                message_list.extend(new_page)
        return message_list
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"A message get error occurred: {error}")
    return None


def idFlatten(page_list=None):
    id_list = []

    if type(page_list) is dict:
        for item in page_list["messages"]:
            id_list.append(item["id"])
        return id_list

    for page in page_list:
        for item in page["messages"]:
            id_list.append(item["id"])
    return id_list


def mailDelete(id):
    creds = tokenUpdate()
    try:
        service = build("gmail", "v1", credentials=creds)

        # Call the Gmail v1 API, retrieve message data.
        del_mail = service.users().messages().delete(userId="me", id=id).execute()
        return del_mail
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"A message get error occurred: {error}")


def mailBatchDelete(ids):
    creds = tokenUpdate()
    try:
        service = build("gmail", "v1", credentials=creds)

        # Call the Gmail v1 API, retrieve message data.
        del_mail = (
            service.users()
            .messages()
            .batchDelete(userId="me", body={"ids": ids})
            .execute()
        )
        return del_mail
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"A message get error occurred: {error}")


def unSubscriber(id):
    creds = tokenUpdate()
    try:
        service = build("gmail", "v1", credentials=creds)

        # Call the Gmail v1 API, retrieve message data.
        message = (
            service.users().messages().get(userId="me", id=id, format="raw").execute()
        )

        # Parse the raw message.
        mime_msg = email.message_from_bytes(base64.urlsafe_b64decode(message["raw"]))

        # redirecting to the unsubscription link
        if "List-Unsubscribe" in mime_msg:
            browser = webbrowser.get('windows-default')
            browser.open_new("https://facebook.com/")
            browser.open_new(mime_msg["List-Unsubscribe"])

        return True
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        return f"A message error occurred: {error}"


def headerExtract2(message_id):
    creds = tokenUpdate()
    try:
        service = build("gmail", "v1", credentials=creds)

        # Call the Gmail v1 API, retrieve message data.
        message = (
            service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )
        return message
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        return f"A message error occurred: {error}"

# msg_list = idFetcher()
# print(msg_list)

# with open('mime_list.py', 'w') as file:
#     file.write(str(msg_list))

# msg = headerExtract("189ab227f84b2442")
# print(msg["decoded"]["List-Unsubscribe"])
# with open('mime_msg.py', 'w') as file:
#     file.write(str(msg['decoded']))

# indeed - '189bb252c8c453f9'
# linkedIn - "189ab227f84b2442"
# TODO unsubcriber, stash, mark as read

with open('mime_msg.py', 'w') as file:
    file.write(str(headerExtract2('189bb252c8c453f9')))


