
# ---------------------------------------------------------------------------------------
import PySimpleGUI as sg
import nettoolkit.facts_finder as ff
from nettoolkit.j2config import PrepareConfig
from pathlib import *
import sys
from inspect import getmembers, isfunction, isclass, isroutine

from nettoolkit.nettoolkit.forms.formitems import *

# ---------------------------------------------------------------------------------------

def btn_j2_gen_exec(obj, i):
	"""executor function

	Args:
		obj (object): frame object 
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	data_file = i['j2_dfile']
	jtemplate_file = i['j2_tfile']
	output_folder = i['j2_output_folder']
	regional_file = i['j2_rfile']
	regional_class = i['j2_reg_class']
	custom_classes = get_custom_classes(i['j2_custom_cls'])
	custom_modules = get_custom_modules(i['j2_custom_fn'])
	# #
	# try:
	PrCfg = PrepareConfig(data_file, jtemplate_file, output_folder, regional_file, regional_class)
	PrCfg.custom_class_add_to_filter(**custom_classes)
	PrCfg.custom_module_methods_add_to_filter(*custom_modules)
	PrCfg.start()
	# except:
	# 	return False
	# return True


def get_import_string(pyFile, importindividuals=False, importmoduleas=''):
	p = Path(pyFile)
	previous_path = p.resolve().parents[1]
	sys.path.insert(len(sys.path), str(previous_path))
	file = p.name.replace(".py", "")
	s = ""
	if importindividuals:
		s = f'from {p.parts[-2]}.{file} import *'
		return s
	if importmoduleas:
		s = f'import {p.parts[-2]}.{file} as {importmoduleas}'
		return s



def j2_custom_reg_exec(obj, i):
	grc = get_regional_class(i['j2_custom_reg'])
	if grc:
		obj.event_update_element(j2_reg_class={'values': grc,  'value': grc[0]})
		return True

def get_regional_class(j2_custom_reg):
	s = get_import_string(j2_custom_reg, importmoduleas='crf')
	exec(s)
	s = '[k[1] for k in getmembers(crf) if isclass(k[1]) and k[0] != "ABSRegion" ]'
	classes = eval(s)
	return classes


# def j2_custom_cls_exec(obj, i):
# 	custom_classes = get_custom_classes(i['j2_custom_cls'])
# 	if custom_classes:
# 		print(custom_classes)
# 		return True

def get_custom_classes(j2_custom_cls):
	s = get_import_string(j2_custom_cls, importmoduleas='cust_cls')
	exec(s)
	s = '{k[0]:k[1] for k in getmembers(cust_cls) if isclass(k[1])}'
	classes = eval(s)
	return classes


# def j2_custom_fn_exec(obj, i):
# 	custom_methods = get_custom_modules(i['j2_custom_fn'])
# 	if custom_methods:
# 		print(custom_methods)
# 		return True

def get_custom_modules(j2_custom_fns):
	j2_custom_fns = j2_custom_fns.split(";")
	lst = []
	for i, j2_custom_fn in enumerate(j2_custom_fns):
		s = get_import_string(j2_custom_fn, importmoduleas=f'cust_fns_{i}')
		exec(s)
		s = f"cust_fns_{i}"
		lst.append(eval(s))
	return lst


def j2_gen_frame():
	"""tab display - generator

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Configurations Generator', font='Bold', text_color="black") ],
		under_line(80),
		# ------------------------------------------------------------------------------------
		[sg.Text('Template file', text_color="yellow"), 
			sg.InputText('', key='j2_tfile'), sg.FilesBrowse(key='btn_j2_tfile') ],
		[sg.Text('Data file', text_color="yellow"), 
			sg.InputText('', key='j2_dfile'), sg.FilesBrowse(key='btn_j2_dfile') ],
		[sg.Text('Output Folder', text_color="yellow"), 
			sg.InputText('', key='j2_output_folder'), sg.FolderBrowse(key='btn_j2_output_folder') ],
		under_line(80),
		# ------------------------------------------------------------------------------------
		[sg.Text('Regional Data Excel [optional]', text_color="black"), 
			sg.InputText('', key='j2_rfile'), sg.FilesBrowse(key='btn_j2_rfile') ],
		[sg.Text('Custom Regional Processing module hook [optional]', text_color="black"), 
			sg.InputText('', key='j2_custom_reg', change_submits=True), sg.FileBrowse(key='btn_j2_custom_reg') ],
		[sg.Text('Select Regional Processing class', text_color="black"), 
			sg.InputCombo([], key='j2_reg_class', size=(20,1)), ],

		under_line(80),
		# ------------------------------------------------------------------------------------
		[sg.Text('Custom classes module(s) hook [optional]', text_color="black"), 
			sg.InputText('', key='j2_custom_cls', change_submits=False), sg.FileBrowse(key='btn_j2_custom_cls') ],
		under_line(80),
		# ------------------------------------------------------------------------------------
		[sg.Text('Custom methods module(s) hook [optional]', text_color="black"), 
			sg.InputText('', key='j2_custom_fn', change_submits=False), sg.FilesBrowse(key='btn_j2_custom_fn') ],
		under_line(80),
		# ------------------------------------------------------------------------------------

		[sg.Button("Generate", change_submits=True, key='btn_j2_gen')],
		[sg.Text('Under Development: GUI Not fully operatable', text_color="black"), ],

		])

# ---------------------------------------------------------------------------------------
