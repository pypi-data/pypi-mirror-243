
# ---------------------------------------------------------------------------------------
import PySimpleGUI as sg
from nettoolkit.pyVig import pyVig, DFGen
import nettoolkit.nettoolkit_db  as nt
import importlib
from pathlib import *
import sys

from nettoolkit.nettoolkit.forms.formitems import *
from nettoolkit.nettoolkit_common import IO

# ---------------------------------------------------------------------------------------

def pv_data_start_exec(obj, i):
	files = i['pv_input_data_files'].split(";")
	dic = {}
	if i['pv_input_data_files']:
		dic['data_file'] = f"{i['py_datafile_output_folder']}/{i['py_datafile']}"
		print(f'Collecting Data and creating cable-matrix..')
		opd = gen_pyvig_excel(files, i, **dic)
		dic.update(opd)
		print(f'Finished..')
	obj.pyVig_dic = dic
	return True

def pv_start_exec(obj, i):
	"""executor function

	Args:
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		dic = obj.pyVig_dic
	except:
		dic = {}
	dic['stencil_folder'] = i['py_stencil_folder']
	dic['default_stencil'] = ".".join(Path(i['py_default_stencil']).name.split(".")[:-1])
	dic['op_file'] =  f"{i['py_output_folder']}/{i['py_op_file']}"
	#
	dic['default_x_spacing'] = float(i['pv_spacing_x'])
	dic['default_y_spacing'] = float(i['pv_spacing_y'])
	dic['line_pattern_style_separation_on'] = i['pv_line_pattern_sep_column'] if i['pv_line_pattern_sep_column'] else None
	dic['line_pattern_style_shift_no'] = int(i['pv_line_pattern_style_shift_number'])
	dic['connector_type'] = i['pv_connector_type']
	dic['color'] = i['pv_line_color']
	dic['weight'] = float(i['pv_line_weight'])
	dic['data_file'] = i['pv_cm_file']
	#
	print(f'Start Generating Visio')
	pyVig(**dic)
	print(f'Finished Generating Visio..')	

	return True



def pv_input_data_frame():
	"""pyVig  - input data

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Generate pyVig Database', font='Bold', text_color="black") ],
		under_line(80),

		### Database ####
		[sg.Text('clean data files: ', text_color="yellow"), 
			sg.InputText('', key='pv_input_data_files'),  
			sg.FilesBrowse(key='pv_input_data_files_btn'),
		],
		under_line(80),
		#
		[sg.Text('output folder:', size=(20, 1), text_color='yellow'), 
			sg.InputText('', key='py_datafile_output_folder'),  
			sg.FolderBrowse(key='py_output_folder_btn'),
		],
		[sg.Text('output filename: ', text_color="yellow"), 
			sg.InputText('', key='py_datafile'),  
		],
		under_line(80),

		[ sg.Button('Generate Database', key='pv_data_start', change_submits=True),],

		])

# ---------------------------------------------------------------------------------------

def pv_input_visio_frame():
	"""pyVig  - input data

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Generate Visio', font='Bold', text_color="black") ],
		under_line(80),

		### Database ####
		[sg.Text('cable-matrix file:', text_color="yellow"), 
			sg.InputText('', key='pv_cm_file', change_submits=True),  
			sg.FileBrowse(key='pv_cm_file_btn')
		],
		under_line(80),

		### Database ####
		[sg.Text('stencils folder :', size=(20, 1), text_color="yellow"), 
			sg.InputText('', key='py_stencil_folder'),  
			sg.FolderBrowse()
		],
		[sg.Text('default stencil file :', size=(20, 1), text_color="yellow"), 
			sg.InputText("", key='py_default_stencil', change_submits=True),
			sg.FileBrowse(key='py_default_stencil_btn')
		],
		#
		[sg.Text('output folder :', size=(20, 1), text_color='black'), 
			sg.InputText('.', key='py_output_folder'),  
			sg.FolderBrowse(key='py_output_folder_btn')
		],
		[sg.Text('output file name :', size=(20, 1), text_color='black'), 
			sg.InputText("pyVig_output.vsd", key='py_op_file', change_submits=True),
		],
		under_line(80),


		### OPTIONS ####
		[ sg.Text('x-axis spacing:', text_color="black"),  sg.InputText(2.5, size=(5, 1), key='pv_spacing_x',),  
		sg.Text('y-axis spacing:', text_color="black"),  sg.InputText(2.5, size=(5, 1), key='pv_spacing_y',),] , 
		under_line(80),
		[ sg.Text('line pattern separate on column:', text_color="black"), sg.InputText("", size=(5, 1),  key='pv_line_pattern_sep_column',),  
		sg.Text('line pattern style shift by:', text_color="black"),  sg.InputText(2, size=(3, 1), key='pv_line_pattern_style_shift_number',), 
		], 
		[ sg.Text('connector (line) type:', text_color="black"),  sg.InputCombo(['straight', 'angled', 'curved'], key='pv_connector_type', size=(10, 1),  default_value='straight', ),  
		sg.Text(' color:', text_color="black"),  sg.InputText('black', size=(10, 1), key='pv_line_color',),  
		sg.Text(' thickness:', text_color="black"),  sg.InputText(1, size=(3, 1), key='pv_line_weight',),  
		],
		under_line(80),

		[ sg.Button('Generate Visio', key='pv_start', change_submits=True),],

		])

# ---------------------------------------------------------------------------------------





# ------------------------------------------------------------------------- 
# Functions
# ------------------------------------------------------------------------- 
def gen_pyvig_excel(files, i, **dic):

	# 1. create DataFrame Object  
	DFG = DFGen(files)

	# 2. add custome attrib/functions						# optional
	DFG.custom_attributes(			
		default_stencil=dic['default_stencil'],
		default_x_spacing=dic['default_x_spacing'],
		default_y_spacing=dic['default_y_spacing'],
		line_pattern_style_separation_on=dic['line_pattern_style_separation_on'],
		line_pattern_style_shift_no=dic['line_pattern_style_shift_no'],
		#
		connector_type=dic['connector_type'],
		color=dic['color'],
		weight=dic['weight'],
	)

	p = Path(i['pv_custom_pkg'])
	previous_path = p.resolve().parents[1]
	sys.path.insert(len(sys.path), str(previous_path))
	file = p.name.replace(".py", "")
	s = f'from {p.parts[-2]}.{file} import *'
	exec(s)

	custom_fn_mandatory_s = f"DFG.custom_functions({i['pv_custom_mandatory_fns']})"
	exec(custom_fn_mandatory_s)

	custom_fn_opt_var_s = f"DFG.custom_var_functions({i['pv_custom_opt_var_fns']})"
	exec(custom_fn_opt_var_s)


	# 3. go thru all provided files,  generate a single pyVig readable Excel file
	DFG.run()

	# # 4. update for custom modifications, provide necessary functions
	# DFG.update(remove_undefined_cabling_entries, add_sheet_filter_columns)
	# opd = {'sheet_filters': get_sheet_filter_columns(DFG.df_dict)}
	# opd['is_sheet_filter'] = True if opd['sheet_filters'] else False
	# CANNOT BE DONE SINCE REQUIRE TO AND FRO PROCESS 

	# 4. Sheet filters
	opd, sheet_filters = {}, {}
	if i['pv_custom_sheet_filters']:
		sheet_filters = eval(i['pv_custom_sheet_filters'])
	opd['sheet_filters'] = sheet_filters	
	opd['is_sheet_filter'] = True if opd['sheet_filters'] else False 

	# 5. Drop Points calculator 
	DFG.calculate_cordinates(sheet_filter_dict=sheet_filters)

	# 6. write out
	nt.write_to_xl(dic['data_file'], DFG.df_dict, index=False, overwrite=True)

	return opd


