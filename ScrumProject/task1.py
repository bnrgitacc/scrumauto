# open project Credentials
import gspread
from oauth2client.service_account import ServiceAccountCredentials

base_url = 'https://projects.purviewservices.com'
api_key = '5fd2f528af9c77b9041a2b7e9c056efdf9783d737b736b070faba362265e08bb'

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('D:\ScrumProject\data\client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open('TestScrumSheet').sheet1
telemedicine = sheet.get_all_records()
print(telemedicine)