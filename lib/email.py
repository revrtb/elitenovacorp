from threading import Thread
from flask import current_app, render_template
from flask_mail import Mail
from time import sleep    

class aMail:

    def __init__(self):
        self.app = None
        self.mail = None

    def initApp(self, app):
        self.app = app
        self.mail = Mail()
        self.mail.init_app(app)

    def send_async_email(self, msg):
        with self.app.app_context():
            self.mail.send(msg)

    def send_email(self, msg):
        thr = Thread(target=self.send_async_email, args=[msg])
        thr.start()
        return thr