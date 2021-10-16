from flask.cli import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

load_dotenv()

SHELTER_PASSWORD = os.getenv("SHELTER_PASSWORD")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
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
                            range="shelters!A1:K10137").execute()
values = result.get('values', [])


def nested_list_to_json(nested_list):

    titles = []
    shelter_list = []
    headers = nested_list[0]
    shelters = nested_list[1:]

    def letter_check(string):
        string = string.replace(")", "").replace(
            "(", "").replace("-", "", 3).replace(" ", "")
        if string.isnumeric():
            return True
        return False
    for title in headers:
        titles.append(title.replace(' ', '_').lower())
    for shelter in shelters:
        if "CA" not in shelter and "@" in shelter[4] and "" not in shelter[2:5]\
                and "" not in shelter[6:10] and len(shelter) == 11 and letter_check(shelter[9]):
            shelt = {}
            for i, data in enumerate(shelter):
                if i != 1 and i != 5 and i != 3:
                    if i == 0:
                        if data == "":
                            data = None
                        elif True not in [char.isdigit() for char in data]:
                            data = None
                        elif shelter[1] != None and True in [char.isdigit() for char in shelter[1]]:
                            data = data + ", " + shelter[1]
                    if i == 4:
                        data = data.lower()
                    if i == 9:
                        if data[0] == "1" and data[1] == "-":
                            data = data.replace("1", "").replace("-", "")
                        data = data.replace(")", "").replace(
                            "(", "").replace("-", "", 3).replace(" ", "")
                        data = "(" + data[:3] + ")-" + \
                            data[3:6] + "-" + data[6:]
                    shelt.update({titles[i]: data})
            shelt.update({"password": SHELTER_PASSWORD})
            shelter_list.append(shelt)
    return shelter_list


all_shelters = nested_list_to_json(values)
