
import PySimpleGUI as sg
from nettoolkit.nettoolkit.forms.formitems import *

def cred_pw_exec(obj, i):
	"""executor function

	Args:
		obj (object): frame object 
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	# try:
	if i['cred_pw'] != '':
		obj.event_update_element(cred_en={'value': i['cred_pw']})
		return True
	# except:
	# 	return None


def exec_cred_frame():
	"""tab display - Credential inputs

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Credentials', font='Bold', text_color="black") ],
		[sg.Text("Username [MechID]:", text_color="yellow"),sg.InputText("", key='cred_un', size=(10,1)),],
		[sg.Text("Password:", text_color="yellow"),sg.InputText("", key='cred_pw', password_char='*', size=(32,1),),],
		[sg.Text("Enable:", text_color="black"),sg.InputText("", key='cred_en',  password_char='*', size=(32,1)),],
		under_line(80),

		[sg.Text('Output Folder', font='Bold', text_color="black") ],
		[sg.Text('select folder:', text_color="yellow"), 
			sg.InputText('', key='cit_op_folder'),  
			sg.FolderBrowse(),
		],
		under_line(80),

		])
