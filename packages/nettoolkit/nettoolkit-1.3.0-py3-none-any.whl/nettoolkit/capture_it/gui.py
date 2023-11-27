
import PySimpleGUI as sg

from nettoolkit.capture_it.forms.cred import *
from nettoolkit.capture_it.forms.options import *
from nettoolkit.capture_it.forms.common_to_all import *
from nettoolkit.capture_it.forms.custom import *

# -----------------------------------------------------------------------------
# Class to initiate UserForm
# -----------------------------------------------------------------------------

class CaptureIT():
	'''CaptureIT - Inititates a UserForm asking user inputs.	'''

	header = 'Capture IT - v1.0.0'

	# Object Initializer
	def __init__(self):
		self.tabs_dic = {
			'cred': exec_cred_frame(),
			'options': exec_options_frame(),
			'custom': exec_custom_frame(),
			'Common': exec_common_to_all_frame(),
			# 'Individual': exec_individual_cmds_frame(),
			# 'Quick Show': exec_quick_show_cmds_frame(),
		}
		self.event_catchers = {
			# 'cred_pw': cred_pw_exec,
			'device_ip_list_file': device_ip_list_file_exec,
			'cisco_cmd_list_file': cisco_cmd_list_file_exec,
			'juniper_cmd_list_file': juniper_cmd_list_file_exec,
			'cit_common': cit_common_exec,
			'custom_cit_file': custom_cit_file_exec,
			'custom_dynamic_cmd_class_name': custom_dynamic_cmd_class_name_exec,
			'generate_facts': generate_facts_exec,
			'custom_ff_file': custom_ff_file_exec,
			'custom_fk_file': custom_fk_file_exec,
			'custom_ff_class_name': custom_ff_name_exec,
			'custom_fk_name': custom_fk_name_exec,

		}

		self.event_updaters = {
			# 'cred_pw',
			'cit_common',
			'device_ip_list_file',
			'cisco_cmd_list_file',
			'juniper_cmd_list_file',
			'custom_cit_file',
			'custom_dynamic_cmd_class_name',
			'generate_facts',
			'custom_ff_file', 'custom_ff_class_name',
			'custom_fk_file', 'custom_fk_name',
		}

		# dynamic variables
		self.custom_dynamic_cmd_class = None   # custom dynamic commands execution class
		self.custom_ff_class = None  # custom facts finder class
		self.custom_fk = {}  # custom facts finder foreign keys
		self.create_form()



	def create_form(self):
		"""initialize the form, and keep it open until some event happens.
		"""    		
		layout = [
			banner(self.header), 
			self.button_pallete(),
			tabs_display(**self.tabs_dic),
		]
		self.w = sg.Window(self.header, layout, size=(800, 700))#, icon='data/sak.ico')
		while True:
			event, (i) = self.w.Read()

			# - Events Triggers - - - - - - - - - - - - - - - - - - - - - - - 
			if event in ('Cancel', sg.WIN_CLOSED) : 
				break
			if event in ('Clear',) : 
				self.clear_fields()
				pass
			if event in self.event_catchers:
				if event in self.event_updaters:
					success = self.event_catchers[event](self, i)	
				else:
					success = self.event_catchers[event](i)
				if not success:
					sg.Popup("Mandatory inputs missing or incorrect.\nPlease refill and resubmit.")

			if event == 'file_md5_hash_check':
				self.event_update_element(file_md5_hash_value={'value': ""})


		self.w.Close()

	def button_pallete(self):
		"""button pallete containing standard OK  and Cancel buttons 

		Returns:
			list: list with sg.Frame containing buttons
		"""    		
		return [sg.Frame(title='Button Pallete', 
				title_color='blue', 
				relief=sg.RELIEF_RIDGE, 
				layout=[
			[button_cancel("Cancel"),
			sg.Button("Clear", change_submits=True,size=(10, 1), key='Clear'),
			],
		] ), ]

	def event_update_element(self, **kwargs):
		"""update an element based on provided kwargs
		"""    		
		for element, update_values in kwargs.items():
			self.w.Element(element).Update(**update_values)

	def clear_fields(self):
		fields = (
			'op_folder', 'cred_en', 'cred_un', 'cred_pw', 
			'device_ip_list_file', 'device_ips',
			'cisco_cmd_list_file', 'cisco_cmds',
			'juniper_cmd_list_file', 'juniper_cmds',
			'custom_cit_file', 'custom_dynamic_cmd_class_name', 'custom_dynamic_cmd_class_str',
			'custom_ff_file', 'custom_ff_class_name', 'custom_ff_class_str',
			'custom_fk_file', 'custom_fk_name','custom_fk_str',
			'append_to', 'common_log_file', 'cred_log_type', 'concurrent_connections', 'visual_progress',

		)
		for field in fields:
			d = {field:{'value':''}}
			self.event_update_element(**d)


	# ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- 




# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
	# # Test UI #
	# u = CaptureIT()
	# from pprint import pprint
	# # pprint(u.custom_dynamic_cmd_class)
	# del(u)
# ------------------------------------------------------------------------------
