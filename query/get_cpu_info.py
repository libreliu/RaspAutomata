import os
from q_base import Query

class Q(Query):
	def get_module_info():
		return {'name' : 'get_cpu_info'}
	def run(self):
		return self.get_cpu_info()
	def get_cpu_info(self):
		with open("/proc/cpuinfo") as f:
			data = f.read()
		cpus = data.count("processor\t:")
		model_name = (data[data.find("model name\t: ")+13:].split("\n"))[0]
		ret = {}
		ret['cpus'] = cpus
		ret['model_name'] = model_name
		ret['rawdata'] = data
		return ret
