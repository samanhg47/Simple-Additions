from flask.cli import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

load_dotenv()

SHELTER_PASSWORD = os.getenv("SHELTER_PASSWORD")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '.keys.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1EEiJVJ_wc1WWy4D0bRMQ8xgewsYukOcfp24tKOnFDBk'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API K10137
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range="states!A1:B51").execute()
values = result.get('values', [])


def integrate_states(list):
    states = []
    for state in list:
        obj = {}
        obj.update({'state': state[0], "shorthand": state[1]})
        states.append(obj)
    return states


states_list = integrate_states(values)
print(states_list)
