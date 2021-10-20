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
                            range="cities!A1:E41755").execute()
values = result.get('values', [])


def integrate_cities(values):
    headers = ["city_name", "state_name", "zipcode", "latitude", "longitude"]
    city_list = []
    for city in values:
        if city[1] != "PR":
            city_info = {}
            for i, title in enumerate(headers):
                if i == 2:
                    city[i] = int(city[i])
                if i > 2:
                    city[i] = float(city[i])
                city_info[title] = city[i]
            city_list.append(city_info)
    return city_list


cities_list = integrate_cities(values)
