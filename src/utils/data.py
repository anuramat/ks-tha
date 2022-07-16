from googleapiclient import discovery
from google.oauth2 import service_account
from os import environ
from pathlib import Path
from enum import Enum


class dimension(Enum):
    rows = "ROWS"
    columns = "COLUMNS"


_scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
range = environ.get("sheet_name")
spreadsheet_id = environ.get("spreadsheet_id")
proj_path = Path(environ.get("proj_path"))
creds = service_account.Credentials.from_service_account_file(
    proj_path / "credentials.json", scopes=_scopes
)
service = discovery.build("sheets", "v4", credentials=creds)
request = (
    service.spreadsheets()
    .values()
    .get(spreadsheetId=spreadsheet_id, range=range, majorDimension=dimension.rows.value)
)


def get_data() -> list[list[str]]:
    """
    returns spreadsheet as list of lists
    range specifications can be found here:
    https://developers.google.com/sheets/api/samples/reading
    """
    response = request.execute()

    return response["values"]

wrapper()
