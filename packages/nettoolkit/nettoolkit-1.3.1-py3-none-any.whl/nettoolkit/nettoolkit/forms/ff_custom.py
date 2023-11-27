
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

def get_variables(file):
	with open(file, 'r') as f:
		lines = f.readlines()
	v = []
	for line in lines:
		spl = line.split()
		if len(spl) > 2 and spl[1] == "=" :
			v.append(spl[0])
	return v


def generate_facts_exec(obj, i):
	disable = not i['generate_facts']
	obj.event_update_element(custom_ff_file={'value': '', 'disabled': disable})
	obj.event_update_element(custom_ff_class_name={'value':[], 'disabled': disable})
	obj.event_update_element(custom_ff_file_button={'disabled': disable})
	obj.event_update_element(custom_ff_class_str={'value': '',})
	obj.event_update_element(custom_fk_file={'value': '', 'disabled': disable})
	obj.event_update_element(custom_fk_name={'value': [], 'disabled': disable})
	obj.event_update_element(custom_fk_file_button={'disabled': disable})
	obj.event_update_element(custom_fk_str={'value': '', })
	return True

def custom_ff_file_exec(obj, i):
	try:
		classes = get_classes(i['custom_ff_file'])
		obj.event_update_element(custom_ff_class_name={'values': classes})
		return True
	except:
		return False


def custom_fk_file_exec(obj, i):
	try:
		v = get_variables(i['custom_fk_file'])
		obj.event_update_element(custom_fk_name={'values': v})
		return True
	except:
		return False

def custom_ff_name_exec(obj, i):
	try:
		p = Path(i['custom_ff_file'])
		previous_path = p.resolve().parents[1]
		sys.path.insert(len(sys.path), str(previous_path))
		file = p.name.replace(".py", "")
		s = f'from {p.parts[-2]}.{file} import {i["custom_ff_class_name"]}'
		obj.event_update_element(custom_ff_class_str={'value': s})
		exec(s)
		obj.custom_ff_class = eval(i["custom_ff_class_name"])
		return True
	except:
		return False

def custom_fk_name_exec(obj, i):
	try:
		p = Path(i['custom_fk_file'])
		previous_path = p.resolve().parents[1]
		sys.path.insert(len(sys.path), str(previous_path))
		file = p.name.replace(".py", "")
		s = f'from {p.parts[-2]}.{file} import {i["custom_fk_name"]}'
		obj.event_update_element(custom_ff_class_str={'value': s})
		exec(s)
		if eval(f'isinstance({i["custom_fk_name"]}, dict)'):
			obj.custom_fk = eval(i["custom_fk_name"])
			return True
		else:
			sg.Popup("incorrect type, variable should be of dictionary type")			
			return False
	except:
		return False


def exec_ff_custom_frame():
	"""tab display - Custom inputs

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		

	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Customize facts', font='Bold', text_color="black") ],

		[sg.Checkbox('customize facts files', key='generate_facts', default=False, text_color='yellow', change_submits=True)],

		[sg.Text('select custom facts-finder package file:'), 
			sg.InputText('', key='custom_ff_file', change_submits=True, disabled=True), sg.FileBrowse(key='custom_ff_file_button', disabled=True),
		],
		[sg.Text('select custom facts-finder class'), sg.InputCombo([], key='custom_ff_class_name', size=(20,1), change_submits=True, disabled=True),], 
		[sg.Text('', key='custom_ff_class_str', text_color='blue',),], 
		[sg.Text(''),], 
		[sg.Text('select custom file having foreign keys dictionary:'), 
			sg.InputText('', key='custom_fk_file', change_submits=True, disabled=True), sg.FileBrowse(key='custom_fk_file_button', disabled=True),
		],
		[sg.Text('select foreign key dictionary variable'), sg.InputCombo([], key='custom_fk_name', size=(20,1), change_submits=True, disabled=True),], 
		[sg.Text('', key='custom_fk_str', text_color='blue'),], 
		under_line(80),

		])
