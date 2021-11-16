from app import app
from flask_mail import Mail,Message

app.config.update(dict(
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'idanga324@gmail.com',
    MAIL_PASSWORD = 'danga1010'
))

mail = Mail(app)

#MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
#MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

def sendEmail(subject,content):
    msg2 = Message(subject, sender='bec2000@gmail.com', recipients=['tadiwacherish@gmail.com'])
    msg2.body = content
    mail.send(msg2)
