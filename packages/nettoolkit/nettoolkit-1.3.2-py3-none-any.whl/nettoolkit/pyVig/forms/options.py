
# ---------------------------------------------------------------------------------------
import PySimpleGUI as sg
from pathlib import *
import sys

from nettoolkit.nettoolkit.forms.formitems import *
# ---------------------------------------------------------------------------------------

def append_description_column(self, i):
	"""add the additional columns for description

	Args:
		i (form_inputs): form elements
	"""    		
	if i['select_col']:
		self.dic['cols_to_merge'].append(i['select_col'])
		mdesc = "\n".join(self.dic['cols_to_merge'])
		updates = { 'appened_cols': {'value': mdesc }}
		self.event_update_element(**updates)


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

		[sg.Text("Device Descriptions:", text_color="darkBlue")],
		[sg.InputCombo([], key='pv_select_col', size=(20,1), change_submits=False),  
		sg.Button("ADD", change_submits=False, key='pv_desc_col_add_btn', disabled=True) ],
		[sg.Text("  details from selected columns will be appended to device details along with hostname in visio")],
		[sg.Text("Appended Columns:")],
		[sg.Multiline("", key='pv_appened_cols', autoscroll=True, size=(20,10), disabled=True) ],
		under_line(80),

		])

# ---------------------------------------------------------------------------------------
