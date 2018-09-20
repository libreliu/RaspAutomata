import subprocess
import re

class ConfigError(Exception):
	pass

class cmd_handler:
	''' Handler class, to wrap cmd activities for agents. '''
	def __init__(self, cfg=None):
		self.cfg=cfg

	def chg_config(cfg):
		self.cfg=cfg

	
	# From https://github.com/python/cpython/blob/master/Lib/shlex.py#L281	
	_find_unsafe = re.compile(r'[^\w@%+=:,./-]', re.ASCII).search

	def shellquote(self, s):
		"""Return a shell-escaped version of the string *s*."""
		if not s:
			return "''"
		if self._find_unsafe(s) is None:
			return s

		# use single quotes, and put single quotes into double quotes
		# the string $'b is then quoted as '$'"'"'b'
		return "'" + s.replace("'", "'\"'\"'") + "'"

	def cmd_to_string(self, cmd):
		''' convert from ['ls', '-l'] to ls "-l" '''
		# print(cmd)
		a = ""
		for i in cmd:
			a = a + self.shellquote(i) + " "
		print(a)
		return a

	def execute(self, cmd, *args):
		''' execute a given command passed in lists (wrapped) 
		    cmd: a list consists of progs & args '''
		try:
			if self.cfg.remote_exec == True:
				return self.exec_r(cmd, *args)  # pass a tuple as variable args
			elif self.cfg.local_exec == True:
				return self.exec_l(cmd, *args)
			else:
				raise ConfigError('RemoteExec & LocalExec options not set')
		except AttributeError:
			raise ConfigError('RemoteExec & LocalExec options not set')

	def exec_r(self, cmd, *args):
		'''
		(From Paramiko Docs)
		Authentication is attempted in the following order of priority:

		The pkey or key_filename passed in (if any)
		key_filename may contain OpenSSH public certificate paths as well as regular private-key paths; when files ending in -cert.pub are found, they are assumed to match a private key, and both components will be loaded. (The private key itself does not need to be listed in key_filename for this to occur - just the certificate.)
		Any key we can find through an SSH agent
		Any “id_rsa”, “id_dsa” or “id_ecdsa” key discoverable in ~/.ssh/
		When OpenSSH-style public certificates exist that match an existing such private key (so e.g. one has id_rsa and id_rsa-cert.pub) the certificate will be loaded alongside the private key and used for authentication.
		Plain username/password auth, if a password was given
		If a private key requires a password to unlock it, and a password is passed in, that password will be used to attempt to unlock the key.
		'''

		import paramiko
		paramiko.util.log_to_file('/tmp/sshout')
		
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
			ssh.connect(self.cfg.hostname, self.cfg.port, self.cfg.username, self.cfg.password, self.cfg.pkey, self.cfg.key_filename, self.cfg.timeout, self.cfg.allow_agent, self.cfg.look_for_keys, self.cfg.compress, self.cfg.sock, self.cfg.gss_auth, self.cfg.gss_kex, self.cfg.gss_deleg_creds, self.cfg.gss_host, self.cfg.banner_timeout, self.cfg.auth_timeout, self.cfg.gss_trust_dns, self.cfg.passphrase)
			
			stdin,stdout,stderr = ssh.exec_command(self.cmd_to_string(cmd),environment=self.cfg.exec_renvvar)
			# stdin.write("Y") #interact with server, typing Y 
			# print(stdout.read())
			# for x in stdout.readlines():
			# print x.strip("n")
			# print('OK\n'%(ip))
			stdo_rd = stdout.read()
			stdr_rd = stderr.read()
			ssh.close()
			return (stdo_rd.decode(self.cfg.exec_charset), stdr_rd.decode(self.cfg.exec_charset), None)
		except:
			raise

	def exec_l(self, cmd, *args):
		r = subprocess.run(cmd, *args, capture_output=True)
		return (r.stdout, r.stderr, r.returncode)
		
if __name__ == '__main__':
	class cfgclass:
		local_exec=False
		remote_exec=True

		hostname="localhost"
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
		

	h = cmd_handler(cfgclass)
	print(h.execute(['ls', '/' , '-l']))
			