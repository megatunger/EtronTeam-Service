from flask import Flask, jsonify
from app.pdf_extractor import pdf2tructure
from app.question_list import select_question

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome to Etron API!'


@app.route('/api/pdf', methods=['POST', 'GET'])
def upload_pdf():
    struct_info = pdf2tructure("app/Profile.pdf")
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
