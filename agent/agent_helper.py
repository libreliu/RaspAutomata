from datetime import date

class Agent:
	def __init__(self, cfg):
		self.cfg = cfg
	
	def run():
		''' Virtual method.
		Return a dict as result. '''

		print("This is mere interface.")
		print("You should create your own instance of it")
	
	def report(self, agent_name, kw):
		''' Report and log to database '''
		#FIXME:Write to file directly currently
		with open("rasp_agent.log") as f:
			f.write(agent_name + " " + str(kw))
		
			