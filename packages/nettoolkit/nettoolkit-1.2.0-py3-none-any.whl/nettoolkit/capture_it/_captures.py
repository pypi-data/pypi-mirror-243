# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import pandas as pd
from nettoolkit.nettoolkit_db import append_to_xl
	
from .common import juniper_add_no_more, visual_print
from ._clp import CLP

# -----------------------------------------------------------------------------
# Captures Class
# -----------------------------------------------------------------------------
class Captures(CLP):
	"""Capture output 

	Args:
		dtype (str): device type
		conn (conn): connection object
		cmds (dict, set, list, tuple): set of commands or commands dictionary 
		path (str): path to store the captured output
		visual_progress (int): scale 0 to 10. 0 being no output, 10 all.
		logger(list): device logging messages list
		cumulative (bool, optional): True/False/both. Defaults to False.
		parsed_output(bool): Need to parse output and generate excel or not.

	Inherits:
		CLP (class): Command Line Processing class

	"""    	

	def __init__(self, dtype, conn, path, visual_progress, logger_list, cumulative=False, parsed_output=False):
		"""Initiate captures

		Args:
			dtype (str): device type
			conn (conn): connection object
			path (str): path to store the captured output
			visual_progress (int): scale 0 to 10. 0 being no output, 10 all.
			logger(list): device logging messages list
			cumulative (bool, optional): True/False/both. Defaults to False.
			parsed_output(bool): Need to parse output and generate excel or not.
		"""    		
		self.logger_list = logger_list
		super().__init__(dtype, conn, path, parsed_output, visual_progress, logger_list)
		self.op = ''
		self.visual_progress = visual_progress
		self.cumulative = cumulative
		self.cumulative_filename = None
		self.initialize_capture = True


	def grp_cmd_capture(self, cmds):
		"""grep the command captures for each commands	
		Unauthorized command will halt execution.

		Args:
			cmds (set, list, tuple): set of commands

		Returns:
			None: None
		"""    		
		banner = self.conn.banner
		#
		if isinstance(cmds, dict):
			commands = cmds[self.dtype] 
		if isinstance(cmds, (set, list, tuple)):
			commands = cmds 
		#
		for cmd  in commands:
			if not self.check_config_authorization(cmd): 
				msg_level, msg = 0, f"UnAuthorizedCommandDetected-{cmd}-EXECUTIONHALTED"
				visual_print(msg, msg_level, self.visual_progress, self.logger_list)

				return None

			# if juniper update no-more if unavailable.
			if self.dtype == 'juniper_junos': 
				cmd = juniper_add_no_more(cmd)
			#
			cc = self.cmd_capture(cmd, self.cumulative, banner, self.initialize_capture)
			self.initialize_capture = False
			try:
				output = cc.output
			except:
				output = f": Error executing command {cmd}"
			cmd_line = self.hn + ">" + cmd + "\n"
			self.op += cmd_line + "\n" + output + "\n\n"
			banner = ""


	def add_exec_logs(self):
		"""adds commands execution `logs` tab to DataFrame
		"""		
		msg_level, msg = 10, f"{self.hn} - adding logs tab to DF"
		visual_print(msg, msg_level, self.visual_progress, self.logger_list)
		self.logger_list.append(msg)
		self.parsed_cmd_df['logs'] = pd.DataFrame(self.cmd_exec_logs)

	def write_facts(self):
		"""writes commands facts in to excel tab
		"""
		try:
			xl_file = self.path + "/" + self.conn.hn + ".xlsx"
			msg_level, msg = 5, f"{self.hn} - writing facts to excel: {xl_file}"
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)

			append_to_xl(xl_file, self.parsed_cmd_df, overwrite=True)
			msg_level, msg = 5, f"{self.hn} - writing facts to excel: {xl_file}...Success!"
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)

		except:
			msg_level, msg = 4, f"{self.hn} - writing facts to excel: {xl_file}...failed!"
			visual_print(msg, msg_level, self.visual_progress, self.logger_list)

		return xl_file

