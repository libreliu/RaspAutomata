import os

SOFT_VERSION = "0.1"


class cmd_handle_conf:
	local_exec=False
	remote_exec=True
	hostname="202.38.70.99"
	port=22
	username=None
	password=None
	pkey=None
	key_filename=None
	#timeout=None
	timeout = 5
	allow_agent=True
	look_for_keys=True
	compress=False
	sock=None
	gss_auth=False
	gss_kex=False
	gss_deleg_creds=True
	gss_host=None
	banner_timeout=None
	auth_timeout=None
	gss_trust_dns=True
	passphrase=None

	# May fail silently, comforming to the settings of SSH Client
	exec_renvvar={'LANG':'C', 'LC_ALL':'en_US.UTF-8'}
	exec_charset="utf-8"

class conui_conf:
	template_path = "/conui/template/"
	main_title = "RaspAutomata ver" + SOFT_VERSION
	info_title = "Information"
	stat_title = "Statistics"

class query_conf:
	def __init__(self):
		self.query_plugin_path = os.path.join(os.getcwd(), "query")

cmd_handle = cmd_handle_conf()
conui = conui_conf()
query = query_conf()