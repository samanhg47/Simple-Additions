from googleapiclient.discovery import build
from google.oauth2 import service_account
from pyasn1.type.univ import Null

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
                            range="shelters!A1:K30").execute()
values = result.get('values', [])


def nested_list_to_json(nested_list):
    titles = []
    shelter_list = []
    headers = nested_list[0]
    shelters = nested_list[1:]
    for title in headers:
        titles.append(title.replace(' ', '_').lower())
    for shelter in shelters:
        if "CA" not in shelter and "" not in shelter[2:5] and "" not in shelter[6:10] and len(shelter) == 11:
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
                        data = data.replace(")", "").replace(
                            "(", "").replace("-", "", 3).replace(" ", "")
                        data = "(" + data[:3] + ")-" + \
                            data[3:6] + "-" + data[6:]
                    shelt.update({titles[i]: data})
            shelt.update({"password": "1234"})
            print(shelt)
            print()
            shelter_list.append(shelt)
    return shelter_list


nested_list_to_json(values)
# print(nested_list_to_json(values))
