import os
import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials


USE_ENV = True
SHOW_URL = True
SHOW_ALL_RECORDS = True
SHARED_WITH = [
    ## {value: "", perm_type: "user", role: "reader", notify: False, email_message: "", with_link: False}
]


def non_empty_list(candidate):
    return candidate and len(candidate) > 0


def non_empty_list_of_lists(candidate):
    return non_empty_list(candidate) and non_empty_list(candidate[0])


def get_creds():
    return get_creds_env() if USE_ENV else get_creds_file()


def get_creds_env(credentials_obj=None, scopes=None):
    if not credentials_obj:
        try:
            credentials_obj = json.loads(os.getenv('GOOGLE_API_SERVICES_JSON'))
        except json.decoder.JSONDecodeError:
            print("Could not read JSON")
            exit(-2)

    if not scopes:
        scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    try:
        return ServiceAccountCredentials._from_parsed_json_keyfile(credentials_obj, scopes)
    except ValueError:
        print("Error: Unable to parse credentials object")
        exit(-1)


def get_creds_file(filename=None, scopes=None):
    if not scopes:
        scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    if not filename:
        filename = "client_secret.json"

    try:
        return ServiceAccountCredentials.from_json_keyfile_name(filename, scopes)
    except ValueError:
        print("Error: Unable to Read Credentials file 'client_secret.json'")
        exit(-1)
    except FileNotFoundError:
        print("Error: Unable to Read Credentials file 'client_secret.json'")
        exit(-1)


def authorize(creds):
    try:
        return gspread.authorize(creds)
    except gspread.exceptions.GSpreadException:
        print("Error: Unable to Authorize with google")
        exit(-2)


def open_by_title(title, client):
    try:
        return client.open(title)
    except gspread.SpreadsheetNotFound:
        return client.create(title)


def open_sheet(spreadsheet, title, init_rows=None):
    if not non_empty_list_of_lists(init_rows):
        init_rows = [["Title"]]

    try:
        return spreadsheet.worksheet(title)
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(
            title,
            len(init_rows),
            max(len(row) for row in init_rows))
        for row in init_rows:
            sheet.insert_row(row)
        return sheet


def program():
    client = authorize(get_creds())
    spreadsheet = open_by_title("Whatever name you like", client)

    sheet = open_sheet(spreadsheet, "Sheet1")
    sheet.append_row([f"Row {sheet.row_count}"])

    if SHOW_URL:
        print(f"Url: {spreadsheet.url}")

    for share in SHARED_WITH:
        spreadsheet.share(**share)

    if SHOW_ALL_RECORDS:
        print(sheet.get_all_records())


if __name__ == '__main__':
    program()
