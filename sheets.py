from __future__ import print_function
import pickle
import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import numpy as np
SERVICE_ACCOUNT_FILE = 'etron-1605966088835-a6ee18c2b12a.json'
NUM_FIELDS = 19
from flask import Flask, request
app = Flask(__name__)

def select_question(field):
    questions = {
        "name": "Tên của bạn là gì?",
        "phone": "Số điện thoại của bạn là gì nhỉ?",
        "address": "Địa chỉ nhà bạn ở đâu?",
        "gender": "Bạn là nam hay nữ?",
        "age": "Năm nay bạn bao nhiêu tuổi?",
        "skills": "Những kỹ năng bạn có là gì?",
        "ot": "Bạn có sẵn sàng làm việc sau giờ làm không?",
        "salary_expectation": "Mức lương mong muốn của bạn là bao nhiêu?"
    }
    if field not in questions:
        return ""
    return questions[field]

id_mail = {
    "wwwlinkedincom/in/chiphuyen": 1,
    "diephang97@gmailcom": 2,
    "wwwlinkedincom/in/bangdo172": 3,
    "tuyenhuy026@gmailcom": 4
}

def select_column(field):
    columns = {
        "name": "B",
        "email": "C",
        "phone": "D",
        "address": "E",
        "gender": "F",
        "education_level": "G",
        "major": "H",
        "university": "I",
        "age": "J",
        "skills": "K",
        "job1": "L",
        "job2": "M",
        "job3": "N",
        "satisfaction": "O",
        "ot": "P",
        "salary_expectation": "Q",
        "languages": "R",
        "churn_prediction": "S"
    }
    if field not in columns:
        return ""
    return columns[field]

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

def write_box(text, user_id, field):
    service = build('sheets', 'v4', credentials=creds)
    data = [[text]]
    body = {
        'values': data
    }
    col = select_column(field)
    cow = user_id + 1
    range_ = 'interview!{}{}:{}{}'.format(col, cow, col, cow)
    print(range)
    result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID, range=range_,
    valueInputOption="RAW", body=body).execute()

@app.route('/cv', methods = ['POST']) 
def export_from_cv():
    # print(request.json)
    user_id = request.json['user_id']
    print(user_id)
    data = ['-']*NUM_FIELDS
    data[0] = user_id
    for rq in request.json['cv']:
        data[rq['id'] + 1] = rq['text']
    range_ = 'interview!A{}:S{}'.format(user_id + 1, user_id + 1)
    export_googlesheet(data=data, range_ = range_)
    return {'status': 200}

@app.route('/missing_field', methods= ['GET'])
def read_missing_fields():
    user_id = int(request.args.get('user_id'))
    range_ = 'interview!A{}:S{}'.format(user_id +1, user_id +1)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_).execute()
    values = result.get('values', [])
    print(values)
    json_res = {}
    json_res['email'] = ''
    print(values)
    return 'a'

if __name__ == '__main__':
    app.run(debug = True, port=5000)