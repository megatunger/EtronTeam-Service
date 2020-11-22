import uuid
import json 

from flask import Flask, jsonify, request
from app.pdf_extractor import pdf2tructure
from app.question_list import select_question
from app.sheet_export import output_export

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome to Etron API!'


@app.route('/api/pdf', methods=['POST', 'GET'])
def upload_pdf():
    uploaded_files = request.files.getlist("file")
    filename = 'tmp/' + str(uuid.uuid4()) + '.pdf'
    # filename = 'app/profile_bangdo.pdf'
    uploaded_files[0].save(filename)
    struct_info = pdf2tructure(filename)
    name = struct_info["name"].split()[0]
    email = struct_info["email"]
    missing_fields = []
    for field in struct_info:
        if struct_info[field] == "":
            question = select_question(field)
            if question == "":
                continue

            missing_fields.append({
                "field": field,
                "question": question.format(name)
            })
    
    user_map_id = json.load(open("app/mail_id.json"))
    if email not in user_map_id:
        user_id = len(user_map_id) + 2
    else:
        user_id = user_map_id[email]
    # print(struct_info)
    output_export(user_id, struct_info)
    return jsonify(
        {"email": email, "missing_fields": missing_fields})


@app.route('/api/question', methods=['POST'])
def upload_question_answer():
    return 'Welcome to Etron API!'


@app.route('/api/processing', methods=['POST'])
def processing():
    return 'Welcome to Etron API!'


if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)
