# Module config 

import smtplib
from email.mime.text import MIMEText

def send_mail(param, content):
    '''
    Require the following:
    param['mail']['fromaddr'] = "your_mail@mail.com"
    param['mail']['toaddrs'] = "emergency@mail.com"
    param['mail']['username'] = "your_mail@mail.com"
    param['mail']['password'] = "your_passwd"
    param['mail']['smtp_server'] = "smtp.mail.com:25"
    '''

    m = param['mail']
    
    server = smtplib.SMTP(m['smtp_server'])
    ip = content['text'] + "\r\n"

    msg = MIMEText(ip, 'plain', 'utf-8')
    msg['Subject'] = content['subject']
    msg['From'] = m['fromaddr']
    msg['To'] = m['toaddrs']

   # try:
    server.set_debuglevel(1)
    server.ehlo()
   # server.starttls()
    server.login(m['username'], m['password'])
    server.sendmail(m['fromaddr'], m['toaddrs'], msg.as_string())
    server.quit()
   # except IOError:
    #    print ('error')

if __name__ == '__main__':
    print("Can't run standalone!")
