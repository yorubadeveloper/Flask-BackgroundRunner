# background_runner.py
from flask_mail import Message
import uuid


class BackgroundRunner:
    def __init__(self, mail, executor):
        self.mail = mail
        self.executor = executor

    def send_email(self, recipient, subject, content):
        msg = Message(subject, sender='your_email@example.com', recipients=[recipient])
        msg.body = content
        self.mail.send(msg)

    def send_email_async(self, recipient, subject, content):
        task_id = uuid.uuid4().hex  # Generate a unique task ID
        self.executor.submit_stored(task_id, self.send_email, recipient, subject, content)
        return task_id

    def task_status(self, task_id):
        if not self.executor.futures.done(task_id):
            return "running"
        self.executor.futures.pop(task_id)
        return "completed"