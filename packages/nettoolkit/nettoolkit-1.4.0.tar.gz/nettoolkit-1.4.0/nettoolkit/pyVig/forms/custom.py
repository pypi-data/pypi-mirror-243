
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

		[sg.Text('select custom pyVig support package file:', text_color='yellow'), 
			sg.InputText('', key='pv_custom_pkg'), 
			sg.FileBrowse(key='pv_custom_pkg_button'),
		],

		[sg.Text('Update Mandatory custom functions below to identify item (device) hierarchical order series and item type series ', text_color='yellow')],
		[sg.Multiline('hierarchical_order=hierarchical_order_series,  ## custom \nitem=sw_type_series,  ## custom', 
			key='pv_custom_mandatory_fns', text_color='blue', size=(80,5)),], 

		[sg.Text('Add Optional custom var functions below (if any)', text_color='black'),], 
		[sg.Multiline('hostname=get_dev_hostname,\nip_address=get_dev_mgmt_ip,\ndevice_model=get_dev_model,\nserial_number=get_dev_serial,', 
			key='pv_custom_opt_var_fns', text_color='black', size=(80,5)),], 

		[sg.Text('Add Sheet Filters (if any) - in python dictionary format', text_color='black'),], 
		[sg.Multiline("""{\n}""", 
			key='pv_custom_sheet_filters', text_color='black', size=(40,5)),], 



		])

# ---------------------------------------------------------------------------------------
