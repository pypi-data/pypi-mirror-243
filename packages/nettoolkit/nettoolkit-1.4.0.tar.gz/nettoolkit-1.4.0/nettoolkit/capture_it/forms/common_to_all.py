
import PySimpleGUI as sg
from nettoolkit.nettoolkit.forms.formitems import *
from nettoolkit.capture_it import capture, quick_display, LogSummary


def cit_common_exec(obj, i):
	devices = i['device_ips']
	devices = [d.strip() for d in devices.split("\n")]
	auth = {'un': i['cred_un'] ,'pw': i['cred_pw'], 'en': i['cred_en']}
	cmds = {
		'cisco_ios': i['cisco_cmds'].split("\n"),
		'juniper_junos': i['juniper_cmds'].split("\n"),
	}
	path = i['cit_op_folder']
	if i['cred_cumulative'] == 'cumulative':
		cumulative = True
	elif i['cred_cumulative'] == 'non-cumulative':
		cumulative = False
	else:
		cumulative = i['cred_cumulative']
	forced_login = i['forced_login']
	parsed_output = i['parsed_output']
	visual_progress = i['visual_progress']
	max_connections = int(i['max_connections']) if i['max_connections'].isnumeric() else 100
	common_log_file = i['common_log_file']
	log_type = i['cred_log_type'] if i['cred_log_type'] else None
	log_print = i['print']
	append_to = f"{path}/{i['append_to']}"
	fg = i['generate_facts']

	# # ---- START CAPTURE ----
	c = capture(
		ip_list=devices,
		auth=auth,    
		cmds=cmds,    
		path=path,    
	)
	# # ----- Key settings -----
	c.cumulative = cumulative
	c.forced_login = forced_login
	c.parsed_output = parsed_output
	if visual_progress: c.visual_progress = visual_progress
	if max_connections: c.max_connections = max_connections
	if log_type: c.log_type = log_type
	if common_log_file and log_type=='common': c.common_log_file = common_log_file

	# # ----- Dynamic commands -----
	if obj.custom_dynamic_cmd_class: 
		c.dependent_cmds(custom_dynamic_cmd_class=obj.custom_dynamic_cmd_class)

	# # ----- facts generations -----
	if fg:
		c.generate_facts(
			CustomDeviceFactsClass=obj.custom_ff_class,
			foreign_keys=obj.custom_fk,
		)

	# # ----- execution -----
	c()

	# # ----- Execution Log Summary -----
	ls_dict = {}
	if append_to: ls_dict['append_to'] = append_to
	if log_print: ls_dict['print'] = log_print
	LogSummary(c, **ls_dict)

	# # ----- Finish -----
	sg.Popup("Capture Task(s) Complete..")
	return True


def device_ip_list_file_exec(obj, i):
	"""executor function

	Args:
		obj (object): frame object 
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if i['device_ip_list_file'] != '':
			obj.event_update_element(device_ips={'value': "calculating..."})
			with open(i['device_ip_list_file'], 'r') as f:
				lns = f.readlines()
			lns = ''.join(lns)
			obj.event_update_element(device_ips={'value': lns})
			return True
	except:
		return None

def cisco_cmd_list_file_exec(obj, i):
	"""executor function

	Args:
		obj (object): frame object 
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if i['cisco_cmd_list_file'] != '':
			obj.event_update_element(cisco_cmds={'value': "calculating..."})
			with open(i['cisco_cmd_list_file'], 'r') as f:
				lns = f.readlines()
			lns = ''.join(lns)
			obj.event_update_element(cisco_cmds={'value': lns})
			return True
	except:
		return None

def juniper_cmd_list_file_exec(obj, i):
	"""executor function

	Args:
		obj (object): frame object 
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if i['juniper_cmd_list_file'] != '':
			obj.event_update_element(juniper_cmds={'value': "calculating..."})
			with open(i['juniper_cmd_list_file'], 'r') as f:
				lns = f.readlines()
			lns = ''.join(lns)
			obj.event_update_element(juniper_cmds={'value': lns})
			return True
	except:
		return None





def exec_common_to_all_frame():
	"""tab display - Credential inputs

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Capture commands Output', font='Bold', text_color="black") ],


		[sg.Text('List of device IPs:', text_color="yellow"),
		sg.Multiline("", key='device_ips', autoscroll=True, size=(15,5), disabled=False),
		],
		[sg.Text('Device IPs list-file:', text_color="black"), 
			sg.InputText('', key='device_ip_list_file', change_submits=True,),
			sg.FileBrowse(),
		],
		under_line(80),

		[sg.Text('List of cisco show commands:', text_color="yellow"),
		sg.Multiline("", key='cisco_cmds', autoscroll=True, size=(50,5), disabled=False),
		],
		[sg.Text('Cisco commands list-file:', text_color="black"), 
			sg.InputText('', key='cisco_cmd_list_file', change_submits=True,),
			sg.FileBrowse(),
		],
		under_line(80),

		[sg.Text('List of juniper show commands:', text_color="yellow"),
		sg.Multiline("", key='juniper_cmds', autoscroll=True, size=(50,5), disabled=False),
		],
		[sg.Text('Juniper commands list-file:', text_color="black"), 
			sg.InputText('', key='juniper_cmd_list_file', change_submits=True,),
			sg.FileBrowse(),
		],
		under_line(80),

		[sg.Button("Capture-it", change_submits=True, key='cit_common')],

		])
