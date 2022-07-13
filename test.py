from googleapiclient import discovery
from google.oauth2 import service_account
import enum


class dimension(enum.Enum):
    rows = "ROWS"
    columns = "COLUMNS"


def get_sheet(
    range: str = "Лист1",
    spreadsheet_id: str = "1oy13To3eyYlNDEs49TekBWFBKLycmoq0-wAjl2kEOdY",
    majorDimension: dimension = dimension.rows,
) -> list[list[str]]:

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ]

    credentials = service_account.Credentials.from_service_account_file(
        "credentials.json", scopes=scopes
    )
    # TODO body
    service = discovery.build("sheets", "v4", credentials=credentials)
    return service.files().watch(fileId=spreadsheet_id, body=body).execute()


def main():
    print(response)


if __name__ == "__main__":
    main()
