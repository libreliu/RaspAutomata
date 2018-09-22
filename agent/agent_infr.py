import socket

def get_net_info():
    '''Get the ip, hostname and others in a dict'''
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("12.8.8.8",80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return {'ip': ip}

if __name__ == '__main__':
    print(get_net_info())

