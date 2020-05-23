import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials


SHOW_URL = True
SHOW_ALL_RECORDS = True
SHARED_WITH = [
    ## {value: "", perm_type: "user", role: "reader", notify: False, email_message: "", with_link: False}
]


def non_empty_list(candidate):
    return candidate and len(candidate) > 0


def non_empty_list_of_lists(candidate):
    return non_empty_list(candidate) and non_empty_list(candidate[0])


def get_creds(filename=None, scopes=None):
    if not scopes:
        scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    if not filename:
        filename = "client_secret.json"

    try:
        return ServiceAccountCredentials.from_json_keyfile_name(filename, scopes)
    except ValueError:
        print("Error: Unable to Read Credentials file 'client_secret.json'")
        os.exit(1)


def authorize(creds):
    try:
        return gspread.authorize(creds)
    except gspread.exceptions.GSpreadException:
        print("Error: Unable to Authorize with google")
        os.exit(2)


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
