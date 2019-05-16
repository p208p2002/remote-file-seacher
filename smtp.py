import smtplib
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

def send_mail(send_from: str, subject: str, text: str,
send_to: list, files= None):

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            ext = f.split('.')[-1:]
            attachedfile = MIMEApplication(fil.read(), _subtype = ext)
            attachedfile.add_header(
                'content-disposition', 'attachment', filename=basename(f) )
        msg.attach(attachedfile)

    #
    with open("./.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    host = cfg['smtp']['host']
    port = cfg['smtp']['port']
    user = cfg['smtp']['user']
    pwd = cfg['smtp']['password']

    smtp = smtplib.SMTP(host=host, port= port)
    smtp.starttls()
    smtp.login(user,pwd)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

#send_mail('p208p2002@gmail.com','TEST2','test',['p208p2002@gmail.com'],['./test.txt'])
