# email_app.py
from flask import Flask, request, jsonify
from flask_mail import Mail
from flask_executor import Executor
from background_runner import BackgroundRunner

app = Flask(__name__)
app.config.from_pyfile('config.py')

mail = Mail(app)
executor = Executor(app)
background_runner = BackgroundRunner(mail, executor)


@app.route('/')
def hello():
    return 'Email Sender App'


@app.route('/send_email', methods=['POST'])
def send_email():
    recipient = request.form.get('recipient')
    subject = request.form.get('subject')
    content = request.form.get('content')

    if not all([recipient, subject, content]):
        return jsonify({"error": "recipient, subject, and content parameters are required"}), 400

    task_id = background_runner.send_email_async(recipient, subject, content)
    return jsonify({"task_id": task_id})


@app.route('/task_status/<int:task_id>')
def task_status(task_id):
    status = background_runner.task_status(task_id)
    return jsonify({"status": status})


if __name__ == '__main__':
    app.run(debug=True)