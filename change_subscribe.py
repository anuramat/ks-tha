from __future__ import print_function

import os.path
from dotenv import dotenv_values

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


def subscribe(file_id: str, channel_id: str, channel_address: str):
    creds = service_account.Credentials.from_service_account_file("credentials.json")

    try:
        service = build("drive", "v3", credentials=creds)

        # Call the Drive v3 API
        body = {"id": channel_id, "type": "webhook", "address": channel_address}
        return service.files().watch(fileId=file_id, body=body).execute()
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    env = dotenv_values(".env")
    subscribe(
        file_id=env["spreadsheet_id"],
        channel_id=env["channel"],
        channel_address="http://85.143.220.82:5000/update",
    )
