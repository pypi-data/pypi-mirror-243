
# ---------------------------------------------------------------------------------------
import PySimpleGUI as sg
import nettoolkit.facts_finder as ff

from nettoolkit.nettoolkit.forms.formitems import *

# ---------------------------------------------------------------------------------------

def btn_ff_gen_exec(obj, i):
	"""executor function

	Args:
		obj (object): frame object 
		i (itemobject): item object of frame

	Returns:
		bool: wheter executor success or not.
	"""	
	try:
		if i['ff_log_files'] != '':
			convert_to_cit = i['ff_convert_to_cit']
			skip_txtfsm = i['ff_skip_txtfsm']
			new_suffix = i['ff_new_suffix']
			rearrange = i['ff_rearrange']
			ffcls = i['custom_ff_class_name']
			#
			CustomDeviceFactsClass = None
			foreign_keys = None
			if ffcls:
				CustomDeviceFactsClass = obj.custom_ff_class
				foreign_keys = obj.custom_fk
			#
			for capture_log_file in i['ff_log_files'].split(";"):
				try:
					generate(capture_log_file, convert_to_cit, skip_txtfsm, new_suffix, rearrange, CustomDeviceFactsClass, foreign_keys)
				except Exception as e:
					print(f"Error : {capture_log_file}... skipped\n{e}")
			return True
	except:
		return None

def btn_ff_gen_frame():
	"""tab display - generator

	Returns:
		sg.Frame: Frame with filter selection components
	"""    		
	return sg.Frame(title=None, 
					relief=sg.RELIEF_SUNKEN, 
					layout=[

		[sg.Text('Facts Generator', font='Bold', text_color="black") ],

		[sg.Text('log files', text_color="yellow"), 
			sg.InputText('', key='ff_log_files'), sg.FilesBrowse(key='btn_ff_log_files') ],
		[sg.Checkbox('convert normal capture file to capture_it format before start', key='ff_convert_to_cit', default=True, text_color='black')],
		[sg.Checkbox('rearrange columns as per standard sequence', key='ff_rearrange', default=True, text_color='black')],
		[sg.Checkbox('skip parsed excel outputs', key='ff_skip_txtfsm', default=True, text_color='black')],
		[sg.Text('clean file suffix', text_color="black"),  sg.InputText('-clean', key='ff_new_suffix',),],
		under_line(80),

		[sg.Button("Generate", change_submits=True, key='btn_ff_gen')],

		])

# ---------------------------------------------------------------------------------------


def generate(capture_log_file, convert_to_cit, skip_txtfsm, new_suffix, rearrange, CustomDeviceFactsClass, foreign_keys):
	hn = capture_log_file.split('/')[-1][:-4]
	# -- cleate an instance --
	cleaned_fact = ff.CleanFacts(
		capture_log_file=capture_log_file, 
		capture_parsed_file=None,
		convert_to_cit=convert_to_cit,
		skip_txtfsm=skip_txtfsm,
		new_suffix=new_suffix,
		use_cdp=False,
	)
	print(f"{hn} -", end='\t')
	# -- execute it --
	cleaned_fact()
	print(f"Cleaning done...,", end='\t')
	# -- custom facts additions --
	if CustomDeviceFactsClass:
		ADF = CustomDeviceFactsClass(cleaned_fact)
		ADF()
		ADF.write()
		print(f"Custom Data Modifications done...,", end='\t')
	# -- rearranging tables columns --
	if rearrange:
		ff.rearrange_tables(cleaned_fact.clean_file, foreign_keys=foreign_keys)
		print(f"Column Rearranged done..., ", end='\t')
	print(f"Facts-Generation Tasks Completed !! {hn} !!\n{'-'*80}")
