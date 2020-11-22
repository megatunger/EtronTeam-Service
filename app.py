from flask import Flask, request, Response, send_file
import DrQA.drqa.reader.predictor as predictor
import json
import requests
import jsonpickle
import ast
from flask_cors import CORS

from sheets import *

app = Flask(__name__)

token = "corenlp"
predictions = predictor.Predictor(model='vn_question_model.mdl', tokenizer=token, normalize=True, embedding_file=None, num_workers=None)

print('loaded')

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

@app.route('/')
def hello_world():
    return 'Welcome to Etron API!'


@app.route('/api/pdf', methods=['POST'])
def upload_pdf():
    return 'Welcome to Etron API!'


@app.route('/api/question', methods=['POST'])
def upload_question_answer():
    email = request.json['email']
    user_id = id_mail[email]
    field = request.json['field']
    long_answer = request.json['answer']
    question = select_question(field)
    rq = {}
    rq['context'] = long_answer
    rq['question'] = question
    res = requests.post(url='http://127.0.0.1:5001/infore/api/question_answering', json=rq)
    print(res.json())
    print(res.json()['answers'][0]['result'])
    print(user_id)
    print(field)
    sheet = write_box(res.json()['answers'][0]['result'], user_id=user_id, field=field)
    print(sheet)
    return 'a'


@app.route('/api/processing', methods=['POST'])
def processing():
    return 'Welcome to Etron API!'


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='localhost')
