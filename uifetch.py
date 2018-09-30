import threading
import do_query

def query_worker(name, dparam, callback):
	do_query.query(name, dparam)

def agent_worker():
	pass

class Fetcher:

	def __init__(self):
		self.working_query_lock = threading.Lock()
		self.working_query = {}

	def query(self, name, dparam):
		return do_query.query(name, dparam)
	
#	def query_async(self, name, dparam, callback):
#		# Spawn a fetcher to do the job
#		t = threading.Thread(target=query_worker, args=(name, dparam.copy, callback))
#		t.start()

	def fetch(self):
		pass

if __name__ == '__main__':
	f = Fetcher()
	print(f.query("get_net_info",{}))

f = Fetcher()