from datetime import date

class agent:
	def __init__(self, cfg):
		self.cfg = cfg
	
	def run():
		pass
	
	def report(self, agent_name, kw):
		''' Report and log to database '''
		#FIXME:Write to file directly currently
		with open("rasp_agent.log") as f:
			f.write(agent_name + " " + str(kw))
		
			