
# ---------------------------------------------------------------------------------------
import PySimpleGUI as sg
from pathlib import *
import sys

from nettoolkit.nettoolkit.forms.formitems import *
# ---------------------------------------------------------------------------------------




def pv_custom_data_frame():
	"""pyVig  - input data

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Customize your data', font='Bold', text_color="black") ],
		under_line(80),

		[sg.Text('select custom pyVig support package file:', text_color='blue'), 
			sg.InputText('', key='pv_custom_pkg'), 
			sg.FileBrowse(key='pv_custom_pkg_button'),
		],

		[sg.Text('Update Mandatory custom functions below to identify item (device) hierarchical order series and item type series ')],
		[sg.Multiline('hierarchical_order= ,\nitem= ,', 
			key='pv_custom_mandatory_fns', text_color='blue', size=(80,5)),], 

		[sg.Text('Add Optional custom var functions below (if any)'),], 
		[sg.Multiline('hostname=get_dev_hostname,\nip_address=get_dev_mgmt_ip,\ndevice_model=get_dev_model,\nserial_number=get_dev_serial,', 
			key='pv_custom_opt_var_fns', text_color='black', size=(80,5)),], 

		[sg.Text('Add Sheet Filters (if any) - in python dictionary format'),], 
		[sg.Multiline("""{\n  'core': 'core', \n  'dist': 'dist',\n  'access': 'access',\n}""", 
			key='pv_custom_sheet_filters', text_color='black', size=(40,5)),], 



		])

# ---------------------------------------------------------------------------------------
