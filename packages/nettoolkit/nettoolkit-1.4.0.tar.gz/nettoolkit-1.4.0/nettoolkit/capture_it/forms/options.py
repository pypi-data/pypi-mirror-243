
import PySimpleGUI as sg
from nettoolkit.nettoolkit.forms.formitems import *


def exec_options_frame():
	"""tab display - Optional inputs

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	cumulative=('cumulative', 'non-cumulative', 'both')
	log_type = (None, 'common', 'individual')
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Options', font='Bold', text_color="black") ],
		[sg.Text('Show Progress Details', text_color="black"), 
		sg.InputCombo([x for x in range(0, 11)], default_value=10, key='visual_progress', size=(5,1)), 
		sg.Text('1-low .. 10-high', text_color="blue"), 
		],
		[sg.Text('Output capture log file type', text_color="black"), sg.InputCombo(cumulative, default_value=cumulative[0], key='cred_cumulative', size=(15,1)), ],
		[sg.Checkbox('Try Forced Login', key='forced_login', default=True, text_color='black')],
		[sg.Checkbox('Excel parsed file', key='parsed_output', default=True, text_color='black')],
		[sg.Text('Max Concurrent Connections', text_color="black"), 
		sg.InputText(100, key='max_connections', size=(5,1) ),
		sg.Text('default:100 - Enter 1 for sequential process', text_color="white"), 
		],
		under_line(80),

		[sg.Text('Logging', font='Bold', text_color="black") ],
		[sg.Text('execution debug log type', text_color="black"), sg.InputCombo(log_type, default_value=None, key='cred_log_type', size=(10,1)),], 
		[sg.Text('execution debug log file name (common):', text_color="black"), sg.InputText('common-debug.log', key='common_log_file'),],
		[sg.Text('') ],
		[sg.Text('summary log filename: ', text_color="black"), sg.InputText('cmds_log_summary.log', key='append_to'),],
		[sg.Checkbox('display console summary on console', key='print', default=True, text_color='black')],
		under_line(80),

		])
