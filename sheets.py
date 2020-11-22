from __future__ import print_function
import pickle
import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import numpy as np
SERVICE_ACCOUNT_FILE = 'etron-1605966088835-a6ee18c2b12a.json'
NUM_FIELDS = 18
from flask import Flask, request
app = Flask(__name__) 

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1fj4L9i3BwGaZscHYvBvxIBY2u94WzkdydrIsJ3CdPQ4'
APIKEY = 'AIzaSyAuOJ3B-MVzrXj1Y2-GyS00C9Izmp282Qg'


def export_googlesheet(data ,range_, sheet_id = SPREADSHEET_ID):
    service = build('sheets', 'v4', credentials=creds)
    # data = np.array(data).T.tolist()
    data = [data]
    body = {
        'values': data
    }
    result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID, range=range_,
    valueInputOption="RAW", body=body).execute()
    print(result)


@app.route('/cv', methods = ['POST']) 
def export_from_cv():
    # print(request.json)
    user_id = request.json['user_id']
    print(user_id)
    data = ['-']*NUM_FIELDS
    data[0] = user_id
    for rq in request.json['cv']:
        data[rq['id'] + 1] = rq['text']
    range_ = 'interview!A{}:R{}'.format(user_id + 1, user_id + 1)
    export_googlesheet(data=data, range_ = range_)
    return 'a'

@app.route('/missing_field', methods= ['GET'])
def read_missing_fields():
    user_id = int(request.args.get('user_id'))
    range_ = 'interview!A{}:R{}'.format(user_id +1, user_id +1)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_).execute()
    values = result.get('values', [])
    print(values)
    return 'a'

if __name__ == '__main__':
    app.run(debug = True, port=5000)