# Google Sheets Experiments

Having some issues with an older Python project that is using Google sheets via `gdata`, so I decided to make a greenfield effort with `gspread`.

Deprecation sucks! Hopefully this one lasts longer

## Setup

You'll need a Google account. A Free one should do, but a g-suite is more ideal.

1. Go to the [Google APIs Console](https://console.developers.google.com/apis/dashboard).
2. Create a *new project*.
3. Click **Enable API**.
4. Search for and enable the Google Drive API, and Google Sheets API.
4. **Create credentials** for a *Web Server* to access *Application Data*.
5. Name the service account, grant it a **Project** *Role* of **Editor**.
6. Download the JSON file.
7. Copy the JSON file to your code directory and rename it to `client_secret.json`

From that point forward, this should just work

## Dependencies

This is an old-person `requirements.txt`, which only requires python & pip.

`pip install -r requirements.txt`

## Running

Once you've completed [Setup](#setup), run with `python gsheet.py`
