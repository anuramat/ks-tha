from googleapiclient import discovery
from google.oauth2 import service_account
from os import environ
from pathlib import Path
from enum import Enum


class dimension(Enum):
    rows = "ROWS"
    columns = "COLUMNS"


_scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def get_sheet(
    creds: service_account.Credentials,
    range: str,
    spreadsheet_id: str,
    dim: dimension = dimension.rows,
) -> list[list[str]]:

    service = discovery.build("sheets", "v4", credentials=creds)

    request = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range, majorDimension=dim.value)
    )
    response = request.execute()

    return response["values"]


def main():
    """
    prints all rows of the document
    """
    proj_path = Path(environ.get("proj_path"))
    creds = service_account.Credentials.from_service_account_file(
        proj_path / "credentials.json", scopes=_scopes
    )
    res = get_sheet(
        creds, environ.get("sheet_name"), environ.get("spreadsheet_id"), dimension.rows
    )

    for l in res:
        print(l)


if __name__ == "__main__":
    main()
