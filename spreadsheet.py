import gspread
from oauth2client.service_account import ServiceAccountCredentials


credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials.json',
    ['https://spreadsheets.google.com/feeds'])
client = gspread.authorize(credentials)


def open_spreadsheet(title):
    return client.open(title)
