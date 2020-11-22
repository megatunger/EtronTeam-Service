from __future__ import print_function
import pickle
import os.path
import numpy as np

from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SERVICE_ACCOUNT_FILE = 'etron-1605966088835-a6ee18c2b12a.json'
NUM_FIELDS = 18

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1fj4L9i3BwGaZscHYvBvxIBY2u94WzkdydrIsJ3CdPQ4'
APIKEY = 'AIzaSyAuOJ3B-MVzrXj1Y2-GyS00C9Izmp282Qg'

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def export_googlesheet(data ,range_, sheet_id = SPREADSHEET_ID):
    service = build('sheets', 'v4', credentials=creds)
    data = [data]
    body = {
        'values': data
    }
    result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID, range=range_,
    valueInputOption="RAW", body=body).execute()
    print(result)

def output_export(user_id, data):
    # data = ['-']*NUM_FIELDS
    data = [user_id] + data
    range_ = 'interview!A{}:R{}'.format(user_id + 1, user_id + 1)
    export_googlesheet(data=data, range_ = range_)

if __name__ == "__main__":
    output_export()