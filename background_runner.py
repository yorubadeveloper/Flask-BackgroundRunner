# background_runner.py
from flask_mail import Message


class BackgroundRunner:
    def __init__(self, mail, executor):
        self.mail = mail
        self.executor = executor

    def send_email(self, recipient, subject, content):
        msg = Message(subject, sender='your_email@example.com', recipients=[recipient])
        msg.body = content
        self.mail.send(msg)

    def send_email_async(self, recipient, subject, content):
        task = self.executor.submit(self.send_email, recipient, subject, content)
        return task.id

    def task_status(self, task_id):
        task = self.executor.futures._state(task_id)
        if task.done():
            return "completed"
        else:
            return "running"