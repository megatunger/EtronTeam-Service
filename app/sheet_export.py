from __future__ import print_function
import pickle
import os.path
import numpy as np

from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SERVICE_ACCOUNT_FILE = 'app/etron-1605966088835-a6ee18c2b12a.json'
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
    list_keys = ["name", "email", "phone", "address", "gender", "education_level", "major", "university", "age", "skills", 
                "job1", "job2", "job3", "satisfaction", "ot", "salary_expectation", "languages", "churn_prediction"]
    format_data = [user_id]
    for key in list_keys:
        format_data.append(data[key])
    range_ = 'interview!A{}:S{}'.format(user_id + 1, user_id + 1)
    export_googlesheet(data=format_data, range_ = range_)

if __name__ == "__main__":
    data = ['-' for _ in range(NUM_FIELDS - 1)]
    data = {}
    list_keys = ["name", "email", "phone", "address", "gender", "education_level", "major", "university", "age", "skills", 
                "job1", "job2", "job3", "satisfaction", "ot", "salary_expectation", "languages", "churn_prediction"]
    for key in list_keys:
        data[key] = "-"
    output_export(1, data)