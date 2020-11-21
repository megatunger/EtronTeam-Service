from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome to Etron API!'


@app.route('/api/pdf', methods=['POST'])
def upload_pdf():
    return 'Welcome to Etron API!'


@app.route('/api/question', methods=['POST'])
def upload_question_answer():
    return 'Welcome to Etron API!'


@app.route('/api/processing', methods=['POST'])
def processing():
    return 'Welcome to Etron API!'


if __name__ == '__main__':
    app.run()
