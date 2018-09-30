import socket
from q_base import Query

class Q(Query):
	def run(self):
		return self.get_net_info()
	def get_net_info(self):
		'''Get the ip, hostname and others in a dict'''
		try: 
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("12.8.8.8",80))
			ip = s.getsockname()[0]
		except OSError:
			ip = "unavailable"
		finally:
			s.close()
		return {'ip': ip}