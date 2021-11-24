from flask.cli import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

load_dotenv()

SHELTER_PASSWORD = os.getenv("SHELTER_PASSWORD")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'google-credentials.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1EEiJVJ_wc1WWy4D0bRMQ8xgewsYukOcfp24tKOnFDBk'

service = build('sheets', 'v4', credentials=creds)

body = [
    ['Alaska', 'AK'],
    ['Alabama', 'AL'],
    ['Arkansas', 'AR'],
    ['Arizona', 'AZ'],
    ['California', 'CA'],
    ['Colorado', 'CO'],
    ['Connecticut', 'CT'],
    ['District of Columbia', 'DC'],
    ['Delaware', 'DE'],
    ['Florida', 'FL'],
    ['Georgia', 'GA'],
    ['Hawaii', 'HI'],
    ['Iowa', 'IA'],
    ['Idaho', 'ID'],
    ['Illinois', 'IL'],
    ['Indiana', 'IN'],
    ['Kansas', 'KS'],
    ['Kentucky', 'KY'],
    ['Louisiana', 'LA'],
    ['Massachusetts', 'MA'],
    ['Maryland', 'MD'],
    ['Maine', 'ME'],
    ['Michigan', 'MI'],
    ['Minnesota', 'MN'],
    ['Missouri', 'MO'],
    ['Mississippi', 'MS'],
    ['Montana', 'MT'],
    ['North Carolina', 'NC'],
    ['North Dakota', 'ND'],
    ['Nebraska', 'NE'],
    ['New Hampshire', 'NH'],
    ['New Jersey', 'NJ'],
    ['New Mexico', 'NM'],
    ['Nevada', 'NV'],
    ['New York', 'NY'],
    ['Ohio', 'OH'],
    ['Oklahoma', 'OK'],
    ['Oregon', 'OR'],
    ['Pennsylvania', 'PA'],
    ['Rhode Island', 'RI'],
    ['South Carolina', 'SC'],
    ['South Dakota', 'SD'],
    ['Tennessee', 'TN'],
    ['Texas', 'TX'],
    ['Utah', 'UT'],
    ['Virginia', 'VA'],
    ['Vermont', 'VT'],
    ['Washington', 'WA'],
    ['Wisconsin', 'WI'],
    ['West Virginia', 'WV'],
    ['Wyoming', 'WY']
]

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().update(
    spreadsheetId=SPREADSHEET_ID, range="states!A1", valueInputOption="RAW", body={"values": body}).execute()
values = result.get('values', [])
