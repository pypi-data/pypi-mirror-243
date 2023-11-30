# --------------------------------------------
# IMPORTS
# --------------------------------------------

from collections import OrderedDict

# -----------------------------------------------------------------------------
# STATIC VAR
# -----------------------------------------------------------------------------
BANNER = '> ~~~ RAW COMMANDS CAPTURE SUMMARY (aholo2000@gmail.com) ~~~ <'

# -----------------------------------------------------------------------------
# LogSummary Class
# -----------------------------------------------------------------------------
class LogSummary():
	"""class generating summary report for the commands log/raw capture

	Args:
		c (conn): connection object
		print (bool, optional): display result summary on screen. Defaults to False.
		write_to (str, optional): filename, writes result summary to file. Defaults to None(i.e. off).
	"""	

	def __init__(self, c, print=False, write_to=None, append_to=None):
		"""class instance initializer

		Args:
			c (conn): connection object
			print (bool, optional): display result summary on screen. Defaults to False.
			write_to (str, optional): filename, writes result summary to file. Defaults to None(i.e. off).
			append_to (str, optional): filename, appends result summary to given file. Defaults to None(i.e. off).
		"""		
		self.s = ""
		self.cmd_exec_logs_all = c.cmd_exec_logs_all
		self.set_cmd_listd_dict(c)
		self.device_type_all = c.device_type_all
		self.ips = c.ips
		#
		self.trim_juniper_no_more()
		self.hosts = self.cmd_exec_logs_all.keys()
		self.add_trailing_space_to_cmd()
		self.add_trailing_space_to_host_result()
		self.convert_device_type_wise_hosts()
		self.s = self.concate_cmd_host_data()
		if print is True: self.print()
		if write_to: self.write(write_to, wa='w')
		if append_to: self.write(append_to, wa='a')

	def set_cmd_listd_dict(self, c):
		"""set command list dictionary for all commands executed for a given connection

		Args:
			c (conn): connection object
		"""		
		self.cmd_list_dict = c.all_cmds
		try:
			self.cmd_list_dict = { dt: sorted(list(set(cmds))) for dt, cmds in c.all_cmds.items() }
		except:
			pass

	@property
	def summary(self):
		"""report summary

		Returns:
			str: Multiline report summary
		"""		
		banner = f'! {"="*len(BANNER)} !\n  {BANNER}  \n! {"="*len(BANNER)} !\n'
		return banner+self.s

	def print(self):
		"""prints report summary on screen
		"""		
		print(self.summary)

	def write(self, file, wa='w'):
		"""writes result summary to file

		Args:
			file (str): filename to write to output result summary
		"""		
		try:
			with open(file, wa) as f:
				f.write(self.s)
				print(f'Info:\tcommands capture log write to {file}.. done')
		except:
			print(f'Info:\tcommands capture log write to {file}.. failed')

	def trim_juniper_no_more(self):
		"""trip juniper commands by removing `| no-more ` word
		"""		
		for host, cmd_exec_logs in self.cmd_exec_logs_all.items():
			for i, item in enumerate(cmd_exec_logs):
				item['command'] = item['command'].replace("| no-more ", "")

	def get_raw_log(self, host_cmd_exec_log, cmd):
		"""get raw log of given command from provided host command execution log list.

		Args:
			host_cmd_exec_log (list): command execution log list of a host
			cmd (str): command for which raw log requires to be returned

		Returns:
			str: returns `success` if raw log was successful else `failed`.  returns `undefined` if undetected or else.
		"""		
		for item in host_cmd_exec_log:
			if item['command'] == cmd:
				if item['raw'] is True:
					return "success"
				elif  item['raw'] is False:
					return "failed"
				else:
					return "undefined"
		return ""

	def get_raw_logs(self, hostname):
		"""get all commands raw logs for given device(hostname)

		Args:
			hostname (str): hostname for which raw logs to be retuned

		Returns:
			list: list of raw log entries
		"""		
		host_cmd_exec_log = self.cmd_exec_logs_all[hostname]
		logs = []
		cmd_list = self.cmd_list_dict[self.device_type_all[hostname]]
		for cmd in cmd_list:
			logs.append(self.get_raw_log(host_cmd_exec_log, cmd))
		return logs


	def get_all_raw_logs(self):
		"""get raw logs for all devices

		Returns:
			dict: dictionary of {device_hostname: raw_log_entries}
		"""		
		logs = OrderedDict()
		for host in self.hosts:
			logs[host] = self.get_raw_logs(host)
		return logs

	def get_max_cmd_length(self, cmd_list):
		"""returns maximum command length from provided cmd_list

		Args:
			cmd_list (list): list of commands

		Returns:
			int: length of maximum length command
		"""		
		max_len = 0
		for cmd in cmd_list:
			cmd_len = len(cmd)
			if cmd_len > max_len:
				max_len = cmd_len
		if max_len<=11: max_len=11
		return max_len

	def add_trailing_space_to_cmd(self):
		"""adds trailing spaces to commands to make all same length. stores them in new trailing_cmd_dict dictionary
		"""		
		self.trailing_cmd_dict = {}
		for dev_type, cmd_list in self.cmd_list_dict.items():
			max_len = self.get_max_cmd_length(cmd_list)
			doubleline = f'+ {"="*max_len} +'
			trailing_cmd_list = [ doubleline, f'| hosts     >{" "*(max_len-11)} |', ]
			trailing_cmd_list.extend([f'| commands V{" "*(max_len-10)} |', doubleline])
			for cmd in cmd_list:
				cmd_len = len(cmd)
				spaces = max_len - cmd_len
				trailing_cmd_list.append(f'| {cmd}{" "*spaces} |')
			trailing_cmd_list.append(doubleline)
			self.trailing_cmd_dict[dev_type] = trailing_cmd_list

	def get_ip(self, hostname, d):
		"""returns ip address of asked hostname from provided dictionary d 

		Args:
			hostname (str): hostname of device
			d (dict): dictionary of all raw logs

		Returns:
			str: ip address for given hostname
		"""		
		return self.ips[list(d.keys()).index(hostname)]

	def add_trailing_space_to_host_result(self):
		"""adds trailing spaces to host results to make all same length. stores them in new trailing_host_dict dictionary 
		"""		
		d = self.get_all_raw_logs()
		max_len_static = 9
		self.trailing_host_dict = {}
		for hn, cmd_results in d.items():
			ip = self.get_ip(hn, d)
			max_len = len(hn) if len(hn) > max_len_static else max_len_static
			if len(ip) > max_len: max_len = len(ip) 
			doubleline = f' {"="*max_len} +'
			self.trailing_host_dict[hn] = [doubleline, f' {hn}{" "*(max_len-len(hn))} |']
			self.trailing_host_dict[hn].extend([f' {ip}{" "*(max_len-len(ip))} |', doubleline])
			for cmd_reulst in cmd_results:
				spaces = max_len - len(cmd_reulst)
				self.trailing_host_dict[hn].append(f' {cmd_reulst}{" "*spaces} |')
			self.trailing_host_dict[hn].append(doubleline)


	def concate_cmd_host_data(self):
		"""concatenates comands and hosts data to generate string summary 

		Returns:
			str: summary report in text format
		"""		
		fs = ''
		for dev_type, devices in self.dev_type_hn_dict.items():
			s = '\n'
			s += dev_type + "\n"
			tclist = self.trailing_cmd_dict[dev_type]
			for i, cmd in enumerate(tclist):
				s += cmd
				for hn in devices:
					thlist = self.trailing_host_dict[hn]
					s += thlist[i]
				s += "\n"
			s += "\n"
			fs += s
		return fs

	def convert_device_type_wise_hosts(self):
		"""distribute hosts as per device type i.e. cisco_ios, juniper_junos etc.. and stores them in a new dictionary dev_type_hn_dict dictionary.

		Returns:
			dict: device type wise dictionary {device_type: [hosts,]}
		"""		
		dev_type_hn_dict = {}		
		for hn, dev_type in self.device_type_all.items():
			if not dev_type_hn_dict.get(dev_type):
				dev_type_hn_dict[dev_type] = []
			dev_type_hn_dict[dev_type].append(hn)
		self.dev_type_hn_dict = dev_type_hn_dict
		return dev_type_hn_dict

# -----------------------------------------------------------------------------
