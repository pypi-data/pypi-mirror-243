"""
Not in use
"""


import PySimpleGUI as sg
from nettoolkit.nettoolkit.forms.formitems import *


def exec_common_cmds_exec(i):
	try:
		pass
		# if (i['ips_create_batch'] != "" 
		# 	and i['pfxs_create_batch'] != "" 
		# 	and i['names_create_batch'] != "" 
		# 	and i['op_folder_create_batch'] != ""
		# 	):
		# 	ips_create_batch = get_list(i['ips_create_batch'])
		# 	pfxs_create_batch = get_list(i['pfxs_create_batch'])
		# 	names_create_batch = get_list(i['names_create_batch'])
		# 	for ip in ips_create_batch:
		# 		success = create_batch_file(pfxs_create_batch, names_create_batch, ip, i['op_folder_create_batch'])
		# 	if success:
		# 		s = 'batch file creation process complete. please verify'
		# 		print(s)
		# 		sg.Popup(s)
		# 	else:
		# 		s = 'batch file creation process encounter errors. please verify inputs'
		# 		print(s)
		# 		sg.Popup(s)
		# 	return True
	except:
		return None

def exec_common_cmds_frame():
	"""tab display - common commands capture for all devices

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Capture IT : ( common commands to all )', font='Bold', text_color="black") ],
		under_line(80),

		[sg.Text("Devices (IP):", text_color="yellow"),],
		[sg.Multiline("", key='ips_common', autoscroll=True, size=(25,10), disabled=False),],
		[sg.Text("Example: \n10.10.10.1\n10.10.30.2,10.10.50.10")],



		[sg.Column([
			]),
		sg.Column([
			[sg.Text("Prefix Names", text_color="yellow")],
			[sg.Multiline("", key='names_create_batch', autoscroll=True, size=(25,10), disabled=False) ],
			[sg.Text("Example: \nVlan-1\nVlan-2,Loopback0")],

			]),
		sg.Column([
			[sg.Text("IP(s)", text_color="yellow")],
			[sg.Multiline("", key='ips_create_batch', autoscroll=True, size=(10,10), disabled=False) ],
			[sg.Text("Example: \n1\n3,4,5")],

			]),
		],
		under_line(80),

		[sg.Text("Entries of Prefixes and Prefix Names should match exactly")],
		[sg.Text("Entries can be line(Enter) or comma(,) separated")],
		under_line(80),
		[sg.Button("Create", size=(10,1),  change_submits=True, key='go_create_batch')],
		under_line(80),

		])
