
# ---------------------------------------------------------------------------------------
import PySimpleGUI as sg

from nettoolkit.forms.formitems import *
from nettoolkit_common import IO

# ---------------------------------------------------------------------------------------

def pv_input_data_exec(i):
	"""executor function

	Args:
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		pass
		# if i['compare_config_file1'] != '' and i['compare_config_file2'] != '':
		# 	text_diff(i['compare_config_file1'], i['compare_config_file2'], i['op_folder_compare_config_text'])
		# 	sg.Popup("Success!")
		# 	return True
	except Exception as e:
		sg.Popup('Failure!')
		return None


def pv_input_data_frame():
	"""facts finder  - input data

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Input your data', font='Bold', text_color="black") ],

		[sg.Text('select database file :', size=(20, 1), text_color="blue"), 
			sg.InputText(self.dic['data_file'], key='data_file', change_submits=True),  
			sg.FileBrowse()],
		[sg.Text('select stencils folder :', size=(20, 1), text_color="blue"), 
			sg.InputText(self.dic['stencil_folder'], key='stencil_folder'),  
			sg.FolderBrowse()],
		[sg.Text('select default stencil file :', size=(20, 1)), 
			sg.InputText("", key='def_stn', change_submits=True),
			sg.FileBrowse()],
		self.under_line(80),
		[sg.Text('x-coordinates col' , size=(20, 1)), sg.InputCombo([], key='x', size=(20,1), disabled=True, change_submits=False)],  
		[sg.Text('y-coordinates col' , size=(20, 1)), sg.InputCombo([], key='y', size=(20,1), disabled=True, change_submits=False)],  

		self.under_line(80),
		[sg.Text('a-device col'      , size=(20, 1)), sg.InputCombo([], key='dev_a', size=(20,1), disabled=True, change_submits=False)],  
		[sg.Text('b-device col'      , size=(20, 1)), sg.InputCombo([], key='dev_b', size=(20,1), disabled=True, change_submits=False)],  

		self.under_line(80),

		# [sg.Text('compare text files (cisco/juniper)', font='Bold', text_color="black") ],
		# under_line(80),

		# [sg.Text('Select first file (text file only):',  text_color="yellow"), 
		# 	sg.InputText(key='compare_config_file1'),  
		# 	sg.FileBrowse()],

		# [sg.Text('Select second file (text file only):',  text_color="yellow"), 
		# 	sg.InputText(key='compare_config_file2'), 
		# 	sg.FileBrowse()],

		# [sg.Text('output folder:', text_color="yellow"), 
		# 	sg.InputText('', key='op_folder_compare_config_text'),  
		# 	sg.FolderBrowse(),
		# ],

		# [sg.Button("Start", change_submits=True, key='go_compare_config_text')],
		# under_line(80),

		# # -----------------------------------------------------------------------------

		# [sg.Text('compare excel files ', font='Bold', text_color="black") ],
		# under_line(80),

		# [sg.Text('Select first file (excel file only):',  text_color="yellow"), 
		# 	sg.InputText(key='compare_config_file3'),  
		# 	sg.FileBrowse()],

		# [sg.Text('Select second file (excel file only):',  text_color="yellow"), 
		# 	sg.InputText(key='compare_config_file4'), 
		# 	sg.FileBrowse()],

		# [sg.Text('output folder:', text_color="yellow"), 
		# 	sg.InputText('', key='op_folder_compare_xl'),  
		# 	sg.FolderBrowse(),
		# ],

		# [sg.Text('tab name:',  text_color="yellow"), 
		# 	sg.InputText(key='compare_config_tab_name'),],
		# [sg.Text('index column nmae:',  text_color="yellow"), 
		# 	sg.InputText(key='compare_config_index_col'),],


		# [sg.Button("Start", change_submits=True, key='go_compare_config_xl')],
		# under_line(80),

		])

# ---------------------------------------------------------------------------------------

