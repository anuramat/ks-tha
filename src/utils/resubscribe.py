from __future__ import print_function

from os import environ
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

_scopes = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


def subscribe(body: dict, service, file_id: str) -> str:
    try:
        return service.files().watch(fileId=file_id, body=body).execute()
    except HttpError as error:
        print(f"subscribe error: {error}")


def unsubscribe(body: dict, service) -> str:
    try:
        return service.channels().stop(body=body).execute()
    except HttpError as error:
        print(f"unsubscribe error: {error}")


def resubscribe():
    """
    Subscribes to google api file change notifications.
    Notifications arrive to update endpoint.
    Subscription is active for an hour and thus needs to be updated.
    """
    proj_path = Path(environ.get("proj_path"))
    creds = service_account.Credentials.from_service_account_file(
        proj_path / "credentials.json", scopes=_scopes
    )
    service = build("drive", "v3", credentials=creds)
    resource_id_filename = "resource_id"
    channel_id = environ.get("channel_id")
    file_id = environ.get("spreadsheet_id")
    resource_id = None
    try:
        with open(proj_path / resource_id_filename, "r") as file:
            resource_id = file.read()
    except FileNotFoundError:
        print("Resource ID file not found (as expected on first subscription)")
    address = "https://" + environ.get("hostname") + environ.get("channel_path")

    body = {
        "kind": "api#channel",
        "type": "webhook",
        "id": channel_id,
        "resourceId": resource_id,
        "address": address,
    }

    if resource_id:
        unsub_response = unsubscribe(body=body, service=service)
        if unsub_response == "":
            print("Successfully unsubscribed")

    sub_response = subscribe(body=body, service=service, file_id=file_id)
    if "resourceId" in sub_response:
        print("Successfully subscribed")
        resource_id = sub_response["resourceId"]
        with open(proj_path / resource_id_filename, "w") as file:
            file.write(resource_id)
