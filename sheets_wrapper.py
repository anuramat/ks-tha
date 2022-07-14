from googleapiclient import discovery
from google.oauth2 import service_account
from dotenv import dotenv_values
from enum import Enum


class dimension(Enum):
    rows = "ROWS"
    columns = "COLUMNS"


def get_sheet(
    range: str,
    spreadsheet_id: str,
    dim: dimension = dimension.rows,
) -> list[list[str]]:

    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    credentials = service_account.Credentials.from_service_account_file(
        "credentials.json", scopes=scopes
    )

    service = discovery.build("sheets", "v4", credentials=credentials)

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
    env = dotenv_values(".env")
    res = get_sheet(env["sheet_name"], env["spreadsheet_id"])

    for l in res:
        print(l)


if __name__ == "__main__":
    main()
