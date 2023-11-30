# -----------------------------------------------------------------------------
import os
from copy import deepcopy
from nettoolkit.nettoolkit_common import *
from nettoolkit.addressing import *

import nettoolkit.facts_finder as ff
from collections import OrderedDict

from ._exec_device import Execute_Device
from .common import visual_print, Log, write_log

# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------
# COMMON methods and variables defining class
# -----------------------------------------------------------------------------------------------
class Execute_Common():
	"""common methods/variables declaration in a Execute Common class

		Args:
			auth (dict): authentication parameters


	Raises:
		Exception: raise exception if any issue with authentication or connections.
	"""	

	def __init__(self, auth):
		"""Initiatlize the connections for the provided iplist, authenticate with provided auth parameters, and execute given commands.
		"""    		
		self.add_auth_para(auth)
		self.set_defaults()
		#

	def __call__(self):
		self.verifications()
		self.start()
		write_log(self.lg, self.log_type, self.common_log_file, self.path)


	def add_auth_para(self, auth):
		"""add authentication parameters to self instance
		
		Args:
			auth (dict): authentication parameters

		Returns:
			None
		"""
		if not isinstance(auth, dict):
			raise Exception(f"authentication parameters needs to be passed as dictionary")
		if not auth.get('un') or auth['un'] == '':
			raise Exception(f"authentication parameters missing with username `un`")
		if not auth.get('pw') or auth['pw'] == '':
			raise Exception(f"authentication parameters missing with password `pw`")
		if not auth.get('en') or auth['en'] == '':
			auth['en'] = auth['pw']
		self.auth = auth

	def set_defaults(self):
		"""setting the default value for optional user input parameters
		"""		
		self.cumulative = True
		self.forced_login = True
		self.parsed_output = False
		self.visual_progress = 10
		self.log_type = None
		self.common_log_file = None
		self.CustomClass = None
		self.fg = False
		self.lg = Log()
		self.max_connections = 100

	def verifications(self):
		"""Verification/Validation of input values
		"""
		if not isinstance(self.visual_progress, (int, float)):
			print(f"visual_progress level to be entered in number, default value (3) selected")
			self.visual_progress = 3
		if not self.cumulative in (True, False, 'both'):
			print( f"cumulative arument is set to {self.cumulative}. No capture-log files will be generated." )
		if self.log_type in ('common', 'both') and not self.common_log_file:
			print( f"common_log_file is missing, debug log will not be generated" )
			self.common_log_file = None
		if not isinstance(self.max_connections, int):
			print(f"Invalid number of `max_connections` defined {self.max_connections}, default 100 taken.")
			self.max_connections = 100




	## variable user inputs ##

	def dependent_cmds(self, custom_dynamic_cmd_class):
		"""Provide dependent commands via a class definition.  A new variable set of commands can be passed
		here using defined custom_dynamic_cmd_class class.  Defined class must have an abstract property called `cmds`. 
		which should return a new set/list of commands to be executed.  A good example of usage of it is - 
		derive the bgp neighbor ip addresses from show ip bgp summary output, and then create new set of commands to see
		advertised route for those neighbor ip addresses.  In this way no need to create a separate set of show commands for multiple
		devices, custom class will take care of generating additional show commands to see advertized routes based on neighbors 
		appear on bgp summary output. ( ofcouse, show ip bgp summary should be there in original show capture ) 		

		Args:
			custom_dynamic_cmd_class (_type_): _description_

		Raises:
			Exception: invalid input `custom_dynamic_cmd_class` for wront types
			Exception: mandatory property missing `cmds` for missing property in provided class
		"""		
		if not hasattr(custom_dynamic_cmd_class, '__class__'):
			raise Exception(f"invalid input `custom_dynamic_cmd_class`,  expected `class`, got `{type(custom_dynamic_cmd_class)}`")
		try:
			custom_dynamic_cmd_class.cmds
		except AttributeError:
			raise Exception(f"mandatory property missing `cmds` in provided class, please implement.")
		self.CustomClass = custom_dynamic_cmd_class


	## other common functions ##


	def is_valid(self, ip):
		"""Validation function to check if provided ip is valid IPv4 or IPv6 address

		Args:
			ip (str): ipv4 or ipv6 address

		Returns:
			bool: True/False based on validation success/fail
		"""    		
		try:
			return ip and Validation(ip).version in (4, 6)
		except:
			msg_level, msg = 0, f'Device Connection: {ip} :: Skipped due to bad Input'
			visual_print(msg, msg_level, self.visual_progress)
			return False


	## generate Facts usings Facts-Finder ##

	def generate_facts(self, CustomDeviceFactsClass=None, foreign_keys={}):
		"""generate excel facts -clean.xlsx file using facts finder

		Args:
			CustomDeviceFactsClass (class, optional): class definition for the modification of excel facts with custom properties. Defaults to None.
			foreign_keys (dict, optional): custom keys(aka: custom columns) here in order to accept them and display in appropriate order. Defaults to {}.

		Raises:
			Exception: Invalid type: foreign_keys if recieved in format other than dict.
		"""		
		self.fg = True
		self.CustomDeviceFactsClass = CustomDeviceFactsClass
		if isinstance(foreign_keys, dict):
			self.foreign_keys = foreign_keys
		else:
			raise Exception(f'Invalid type: foreign_keys: required `dict` got {type(foreign_keys)}')


	def ff_sequence(self, ED, CustomDeviceFactsClass, foreign_keys):
		"""facts finder execution sequences

		Args:
			ED (Execute_Device): Execute_Device class instance post capture finishes
			CustomDeviceFactsClass (class): class definition for the modification of excel facts with custom properties.
			foreign_keys (_type_): custom keys(aka: custom columns) 
		"""	
		# -- cleate an instance --
		cleaned_fact = ff.CleanFacts(
			capture_log_file=ED.cumulative_filename, 
			capture_parsed_file=None,
			convert_to_cit=False,
			skip_txtfsm=True,
			new_suffix='-clean',
			use_cdp=False,
		)
		print(f"{ED.cumulative_filename.split('/')[-1][:-4]} -", end='\t')
		# -- execute it --
		cleaned_fact()
		print(f"Cleaning done...,", end='\t')
		# -- custom facts additions --
		if CustomDeviceFactsClass:
			ADF = CustomDeviceFactsClass(cleaned_fact)
			ADF()
			ADF.write()
			print(f"Custom Data Modifications done...,", end='\t')
		# -- rearranging tables columns --
		ff.rearrange_tables(cleaned_fact.clean_file, foreign_keys=foreign_keys)
		print(f"Column Rearranged done..., ", end='\t')
		print(f"Facts-Generation Tasks Completed !! {ED.hostname} !!\n{'-'*80}")


# -----------------------------------------------------------------------------------------------
# Execute class - capture_it - for common commands to all devices
# -----------------------------------------------------------------------------------------------

class Execute_By_Login(Multi_Execution, Execute_Common):
	"""Execute the device capture by logging in to device.

	Args:
		ip_list (set, list, tuple): set of ip addresses to be logging for capture
		auth (dict): authentication parameters ( un, pw, en)
		cmds (set, list, tuple): set of commands to be captured
		path (str): path where output(s), logs(s) should be stored.

	Properties:
		cumulative (bool, optional): True: will store all commands output in a single file, False will store each command output in differet file. Defaults to False. and 'both' will do both.
		forced_login (bool, optional): True: will try to ssh/login to devices even if ping respince fails. False will try to ssh/login only if ping responce was success. (default: False)
		parsed_output (bool, optional): True: will check the captures and generate the general parsed excel file. False will omit this step. No excel will be generated in the case. (default: False)
		visual_progress (int, optional): 0 will not show any progress, 10 will show all progress (default=3).
		log_type (str): what type of log output requires. choices are = common, individual, both
		common_log_file (str): output file name of a common log file
		max_connections (int, optional): 100: manipulate how many max number of concurrent connections to be establish. default is 100.
		CustomClass (class): Custom class definitition to execute additional custom commands

	Raises:
		Exception: raise exception if any issue with authentication or connections.

	"""    	

	def __init__(self, ip_list, auth, cmds, path="."):
		"""Initiatlize the connections for the provided iplist, authenticate with provided auth parameters, 
		and execute given commands.
		"""    		
		Execute_Common.__init__(self, auth)
		self.devices = STR.to_set(ip_list) if isinstance(ip_list, str) else set(ip_list)
		self.cmds = cmds
		self.all_cmds = deepcopy(self.cmds)
		self.path = path
		#
		self.ips = []
		if not isinstance(cmds, dict):
			raise Exception("commands to be executed are to be in proper dict format")
		self.cmd_exec_logs_all = OrderedDict()
		self.device_type_all = OrderedDict()
		#
		super().__init__(self.devices)



	def execute(self, ip):
		"""execution function for a single device. hn == ip address in this case.

		Args:
			ip (str): ip address of a reachable device
		"""
		# - capture instance -
		ED = Execute_Device(ip, 
			auth=self.auth, 
			cmds=self.cmds, 
			path=self.path, 
			cumulative=self.cumulative,
			forced_login=self.forced_login, 
			parsed_output=self.parsed_output,
			visual_progress=self.visual_progress,
			logger=self.lg,
			CustomClass=self.CustomClass,
			fg=self.fg,
			)

		# - capture logs -
		if self.log_type and self.log_type.lower() in ('individual', 'both'):
			self.lg.write_individuals(self.path)
		self.cmd_exec_logs_all[ED.hostname] = ED.cmd_exec_logs
		self.device_type_all[ED.hostname] =  ED.dev.dtype
		self.ips.append(ip)

		# - update all cmds
		self.update_all_cmds(ED)

		# - facts generations -
		if self.fg: self.ff_sequence(ED, self.CustomDeviceFactsClass, self.foreign_keys)


	def update_all_cmds(self, ED):
		"""update executed commands for all commands dictionary 

		Args:
			ED (Execute_Device): Device Execution object instance
		"""		
		dt = ED.dev.dtype
		self.all_cmds[dt].extend(ED.all_cmds[dt])



# -----------------------------------------------------------------------------------------------
# Execute class - capture_it - for selected individual commands for each device(s)
# -----------------------------------------------------------------------------------------------
class Execute_By_Individual_Commands(Multi_Execution, Execute_Common):
	"""Execute the device capture by logging in to device and running individual commands on to it.

	Args:
		auth (dict): authentication parameters ( un, pw, en)
		dev_cmd_dict: dictionary of list {device_ip:[commands list,]}
		path (str): path where output(s), logs(s) should be stored.

	Properties:
		cumulative (bool, optional): True: will store all commands output in a single file, False will store each command output in differet file. Defaults to False. and 'both' will do both.
		forced_login (bool, optional): True: will try to ssh/login to devices even if ping respince fails. False will try to ssh/login only if ping responce was success. (default: False)
		parsed_output (bool, optional): True: will check the captures and generate the general parsed excel file. False will omit this step. No excel will be generated in the case. (default: False)
		visual_progress (int, optional): 0 will not show any progress, 10 will show all progress (default=3).
		log_type (str): what type of log output requires. choices are = common, individual, both
		common_log_file (str): output file name of a common log file
		max_connections (int, optional): 100: manipulate how many max number of concurrent connections to be establish. default is 100.
		CustomClass (class): Custom class definitition to execute additional custom commands

	Raises:
		Exception: raise exception if any issue with authentication or connections.

	"""    	

	def __init__(self, auth, dev_cmd_dict, path='.'):
		"""Initiatlize the connections for the provided iplist, authenticate with provided auth parameters, 
		and execute given commands.
		"""
		#
		Execute_Common.__init__(self, auth)
		#
		self.verify_dev_cmd_dict(dev_cmd_dict)
		self.add_devices(dev_cmd_dict)
		self.path = path
		self.individual_device_cmds_dict(dev_cmd_dict)
		#
		self.ips = []
		self.cmds = {}
		self.cmd_exec_logs_all = OrderedDict()
		self.device_type_all = OrderedDict()
		#
		super().__init__(self.devices)


	def verify_dev_cmd_dict(self, dev_cmd_dict):
		"""Verify device commands dictionary `dev_cmd_dict` format and values. and raises Exceptions for errors.
		dev_cmd_dict dictionary keys are to be from either of non-iterable type such as (string, tuple, set).
		dev_cmd_dict dictionary values are to be from either of iterable type such as (list, set, tuple, dict).

		Args:
			dev_cmd_dict (dict): device commands dictionary

		Returns:
			None
		"""
		if not isinstance(dev_cmd_dict, dict):
			raise Exception(f"`capture_individual` requires `dev_cmd_dict` parameter in dictionary format")
		for ip, cmds in dev_cmd_dict.items():
			if isinstance(ip, (tuple, set)):
				for x in ip:
					if not isinstance(addressing(x), IPv4):
						raise Exception(f"`dev_cmd_dict` key expecting IPv4 address, received {ip}")
			elif isinstance(ip, str) and not isinstance(addressing(ip), IPv4):
				raise Exception(f"`dev_cmd_dict` key expecting IPv4 address, received {ip}")
			if not isinstance(cmds, (list, set, tuple, dict)):
				raise Exception(f"`dev_cmd_dict` values expecting iterable, received {cmds}")

	def add_devices(self, dev_cmd_dict):
		"""check device commands dictionary and returns set of devices

		Args:
			dev_cmd_dict (dict): device commands dictionary

		Returns:
			None
		"""
		devs = set()
		for ip, cmds in dev_cmd_dict.items():
			if isinstance(ip, (tuple, set)):
				for x in ip:
					devs.add(x)
			elif isinstance(ip, str):
				devs.add(ip)
		self.devices = devs

	def individual_device_cmds_dict(self, dev_cmd_dict):
		"""check device commands dictionary and sets commands list for each of device

		Args:
			dev_cmd_dict (dict): device commands dictionary

		Returns:
			None
		"""
		self.dev_cmd_dict = {}
		for device in self.devices:
			if not self.dev_cmd_dict.get(device):
				self.dev_cmd_dict[device] = set()
			for ips, cmds in dev_cmd_dict.items():
				if isinstance(ips, (tuple, set, list)):
					for ip in ips:
						if device == ip:
							self.add_to(ip, cmds)
				if isinstance(ips, str):
					if device == ips:
						self.add_to(ips, cmds)

	def add_to(self, ip, cmds):
		"""adds `cmds` to the set of commands for given ip in device commands dictionary 

		Args:
			ip (str): ip address of device
			cmds (set): set of commands to be added for ip

		Returns:
			None
		"""
		cmds = set(cmds)
		self.dev_cmd_dict[ip] = self.dev_cmd_dict[ip].union(cmds)

	def execute(self, ip):
		"""execution function for a single device. hn == ip address in this case.

		Args:
			ip (str): ip address of a reachable device
		"""
		cmds = sorted(self.dev_cmd_dict[ip])
		# - capture instance -
		ED = Execute_Device(ip, 
			auth=self.auth, 
			cmds=cmds, 
			path=self.path, 
			cumulative=self.cumulative,
			forced_login=self.forced_login, 
			parsed_output=self.parsed_output,
			visual_progress=self.visual_progress,
			logger=self.lg,
			CustomClass=self.CustomClass,
			fg=self.fg,
			)
		# - log capture -
		if self.log_type and self.log_type.lower() in ('individual', 'both'):
			self.lg.write_individuals(self.path)
		self.cmd_exec_logs_all[ED.hostname] = ED.cmd_exec_logs
		self.device_type_all[ED.hostname] =  ED.dev.dtype
		self.ips.append(ip)
		#
		if not self.cmds.get(ED.dev.dtype):
			self.cmds[ED.dev.dtype] = set()
		self.cmds[ED.dev.dtype] = self.cmds[ED.dev.dtype].union(set(cmds))
		# - facts generation -
		if self.fg: self.ff_sequence(ED, self.CustomDeviceFactsClass, self.foreign_keys)



# -----------------------------------------------------------------------------------------------
