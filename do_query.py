import importlib
import config
import sys

__is_imported__ = {}

def query(name, dparam):
	# check if it's imported
	if __is_imported__.get(name) != None:
		return __is_imported__.get(name).run()
	# import and create an instance
	# Note: Specify the path of the module dir
	sys.path.append(config.query.query_plugin_path)
	mod = importlib.import_module(name)
	__is_imported__[name] = mod.Q()
	return __is_imported__.get(name).run()

if __name__ == "__main__":
	print(query("get_cpu_info", {}))