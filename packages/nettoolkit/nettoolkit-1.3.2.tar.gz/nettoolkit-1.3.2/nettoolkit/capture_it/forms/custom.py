
import PySimpleGUI as sg
from nettoolkit.nettoolkit.forms.formitems import *
from pathlib import *
import sys


def get_classes(file):
	with open(file, 'r') as f:
		lines = f.readlines()
	classes = [ line.strip().split()[1].split("(")[0] 
				for line in lines
				if line.strip().startswith('class ') ]
	return classes

def custom_cit_file_exec(obj, i):	
	try:
		classes = get_classes(i['custom_cit_file'])
		obj.event_update_element(custom_dynamic_cmd_class_name={'values': classes})
		return True
	except:
		return False


def custom_dynamic_cmd_class_name_exec(obj, i):
	try:
		p = Path(i['custom_cit_file'])
		previous_path = p.resolve().parents[0]
		sys.path.insert(len(sys.path), str(previous_path))
		file = p.name.replace(".py", "")
		s = f'from {file} import {i["custom_dynamic_cmd_class_name"]}'
		obj.event_update_element(custom_dynamic_cmd_class_str={'value': s})
		exec(s)
		obj.custom_dynamic_cmd_class = eval(i["custom_dynamic_cmd_class_name"])
		return True
	except:
		return False






def exec_custom_frame():
	"""tab display - Custom inputs

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		

	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('custom dynamic commands class', font='Bold', text_color="black") ],

		[sg.Text('select custom package file:'), 
			sg.InputText('', key='custom_cit_file', change_submits=True,), sg.FileBrowse(),
		],
		[sg.Text('select custom class'), sg.InputCombo([], key='custom_dynamic_cmd_class_name', size=(10,1), change_submits=True),], 
		[sg.Text('', key='custom_dynamic_cmd_class_str', text_color='blue'),], 
		under_line(80),






		])
