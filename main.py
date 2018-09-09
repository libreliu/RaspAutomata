from query.get_net_info import *
from report.send_mail import *

import sys, getopt

def usage():
    print("Usage: main.py 123456")


def parse_input():
    param = {'mail': {'fromaddr' : '1050011904@qq.com', 'toaddrs' : 'jauntyliu@mail.ustc.edu.cn', 'username': '1050011904@qq.com', 'smtp_server' : 'smtp.qq.com:25'}}
    param['mail']['password'] = sys.argv[1] 
    return param;

info = get_net_info()
print (info)
content = {}
content['subject'] = "IP | RaspAutomata"
content['text'] = get_net_info()['ip']
send_mail(parse_input(),content) 


