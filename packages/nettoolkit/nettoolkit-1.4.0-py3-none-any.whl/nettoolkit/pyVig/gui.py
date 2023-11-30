"""pyVig GUI Form Production
"""

# -----------------------------------------------------------------------------
import PySimpleGUI as sg
import pandas as pd
from pprint import pprint

# -----------------------------------------------------------------------------
declaration = """
 ~~~~ IMPORTANT INFORMATION ~~~~
 This program was tested with MS-Visio Professional 2013, 2016.
 It may or may not work depending on other older visio version.
 File save feature is not working in visio version.
 Remember to save the file manually.

 Macros and vBA scripting requires to be enabled in visio
 in order to access the visio components.
 select 'Enable all macros' and, check 'Trust access to vBA'
 from trust center setting of MS-visio.

 Please reachout to me, @ aholo2000@gmail.com for any Qs.
 Owned and mainained by: [Aliasgar Lokhandwala]
"""

# -----------------------------------------------------------------------------
# Class to initiate UserForm
# -----------------------------------------------------------------------------

class UserForm():
	'''Inititates a UserForm asking user inputs.	'''
	version  = 'Visio Generator : gui ver: 0.0.11'
	header = 'Visio Generator'

	# Object Initializer
	def __init__(self):
		self.boot = False
		self.dic = {
			# mandatories
			'stencil_folder':"",
			'data_file' : "",

			# optionals
			'default_stencil': '',
			'op_file': 'output.vsdx',

			'x': 'x-axis',
			'y': 'y-axis',
			'dev_a': 'a_device',
			'dev_b': 'b_device',
			#
			'cols_to_merge': [],
			'is_sheet_filter': True,
			'sheet_filters':{},	
			'filter_on_include_col': False,
			'filter_on_cable': True,
			}
		self.create_form()

	def __repr__(self):
		return f'User : {self.dic["un"]}'

	def __getitem__(self, key):
		'''get an item from parameters'''
		try:
			return self.dic[key]
		except: return None

	def enable_boot(self):
		"""defines whether it is good to go ahead or not"""
		self.boot = False
		self.w.Element('Go').Update(disabled=False)

	@property
	def blank_line(self): 
		"""to insert a blank row

		Returns:
			list: blank row
		"""		
		return [sg.Text(''),]
	def item_line(self, item, length):
		"""to draw a line with provided character or repeat a character for n-number of time

		Args:
			item (str): character
			length (int): to repeat the character

		Returns:
			list: list with repeated item Text
		"""    	
		return [sg.Text(item*length)]
	def under_line(self, length): 
		"""To draw a line

		Args:
			length (int): character length of line

		Returns:
			list: underline row
		"""		
		return [sg.Text('_'*length)]
	def button_ok(self, text, **kwargs):  
		"""Insert an OK button of regular size. provide additional formating as kwargs.

		Args:
			text (str): Text instead of OK to display (if need)

		Returns:
			sg.OK: OK button
		"""		
		return sg.OK(text, size=(10,1), **kwargs)	
	def button_cancel(self, text, **kwargs):
		"""Insert a Cancel button of regular size. provide additional formating as kwargs.

		Args:
			text (str): Text instead of Cancel to display (if need)

		Returns:
			sg.Cancel: Cancel button
		"""    	  
		return sg.Cancel(text, size=(10,1), **kwargs)
	def banner(self):
		"""Banner / Texts with bold center aligned fonts

		Returns:
			list: list with banner text
		"""    		
		return [sg.Text(self.version, font='arialBold', justification='center', size=(768,1))] 

	def button_pallete(self):
		"""button pallete containing standard OK  and Cancel buttons 

		Returns:
			list: list with sg.Frame containing buttons
		"""    		
		return [sg.Frame(title='Button Pallete', 
				title_color='blue', 
				relief=sg.RELIEF_RIDGE, 
				layout=[
			[self.button_ok("Go", bind_return_key=True), self.button_cancel("Cancel"),],
		] ), ]

	def create_form(self):
		"""initialize the form, and keep it open until some event happens.
		"""    		
		self.tabs()
		layout = [
			self.banner(), 
			self.button_pallete(),
			self.tabs_display(),
		]
		self.w = sg.Window(self.header, layout, size=(1000,700))#, icon='data/sak.ico')
		while True:
			event, (i) = self.w.Read()
			# - Events Triggers - - - - - - - - - - - - - - - - - - - - - - - 
			if event == 'Cancel': 
				del(self.dic)
				break
			if event == 'Go': 
				if self.check_basics(i): 
					self.event_update_Go(i)
			if event == 'is_sheet_filter': self.event_update_filter(i)
			if event == 'filt_col_add': self.sheet_filter_add_col_value(i)
			if event == 'def_stn': self.update_default_stencil(i)
			if event == 'enable_description_merge': self.update_description_col_dropbox(i)
			if event == 'desc_col_add': self.append_description_column(i)
			if event == 'data_file': 
				self.update_cabling_sheet_columns(i)
				self.update_devices_sheet_columns(i)


			# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
			if self.boot:
				self.w.Element('Go').Update(disabled=True)
				break
		self.w.Close()

	def tabs(self, **kwargs):
		"""create tab groups for provided kwargs

		Returns:
			sg.TabGroup: Tab groups
		"""    		
		tabs = []
		for k, v in kwargs.items():
			tabs.append( sg.Tab(k, [[v]]) )
		return sg.TabGroup( [tabs] )

	def tabs_display(self):
		"""define tabs display

		Returns:
			list: list of tabs
		"""    		
		tabs_dic = {
			'Declaration': self.show_declaration(),
			'Input Your Data': self.input_data(), 
			'Apply Filters': self.select_filters(),
			'Other Options': self.other_options(),

		}
		return [self.tabs(**tabs_dic),]

	def event_update_Go(self, i):
		"""execute when Go button pressed

		Args:
			i (form_inputs): form inputs reader
		"""    		
		exception_key_list = ('add exception list here', 'sheet_filters',
			'filt_col_key', 'filt_col_value', 'filt_col_add',
			'cols_to_merge', 'cms',
			'def_stn', 'default_stencil',)
		self.boot = True
		for k in self.dic:
			if k in exception_key_list: continue
			self.dic[k] = i[k]

	def input_data(self):
		"""input data tab details display

		Returns:
			sg.Frame: Frame with input data components
		"""    		
		return sg.Frame(title='User Input / Database', 
						title_color='red', 
						# size=(500, 4), 
						key='user_input',						
						relief=sg.RELIEF_SUNKEN, 
						layout=[
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
			])

	def select_filters(self):
		"""selection of filters tab display

		Returns:
			sg.Frame: Frame with filter selection components
		"""    		
		return sg.Frame(title='Database Filters', 
						title_color='red', 
						# size=(500, 4), 
						key='database_filters',						
						relief=sg.RELIEF_SUNKEN, 
						layout=[
			[sg.Checkbox('Enable filter on matching cables', default=self.dic['filter_on_cable'], key='filter_on_cable', change_submits=False) ],
			[sg.Text("  **Enabling this will omit the devices which doen't participate in cabling,")],
			[sg.Text("  Disabling will include all devices irrespective of their existance in cabling")],
			self.under_line(80),
			[sg.Text("DATA Filters",  text_color='darkBlue', font='arialBold')],
			[sg.Checkbox('Filter data based on `include` col == `x`', default=self.dic['filter_on_include_col'], key='filter_on_include_col', change_submits=False) ],
			[sg.Checkbox('Enable multi-sheet layout ', default=False, key='is_sheet_filter', change_submits=True) ],
			[sg.Text("  **sheet name will be column name mentioned below, \n and sheet-data will be choosen based on matching values given in that particular column")],
			[sg.Text("Column Name"), 
			sg.InputCombo([], key='filt_col_key', size=(20,1), disabled=True, change_submits=False),  
			sg.Text(" == "), sg.InputText("", key='filt_col_value', size=(12, 1), disabled=True), sg.Text(" Column Value "),
			sg.Button("ADD", change_submits=False, key='filt_col_add', disabled=True)
			],
			[sg.Text("Applied Filters:")],
			[sg.Multiline("", key='merged_filt_cols', autoscroll=True, size=(20,10), disabled=True) ]

			])

	def other_options(self):
		"""other options tab details display

		Returns:
			sg.Frame: Frame with other option components
		"""    		
		return sg.Frame(title='Other Options', 
						title_color='red', 
						# size=(500, 4), 
						key='oth_options',						
						relief=sg.RELIEF_SUNKEN, 
						layout=[
			[sg.Text("Output Filename",), sg.InputText(self.dic['op_file'], key='op_file', size=(12, 1), disabled=True)],
			self.under_line(80),
			[sg.Text("Device Descriptions:", text_color="darkBlue")],
			[sg.Checkbox('Add Columns to Descriptions ', default=False, key='enable_description_merge', change_submits=True) ],
			[sg.InputCombo([], key='select_col', size=(20,1), disabled=True, change_submits=False),  
			sg.Button("ADD", change_submits=False, key='desc_col_add', disabled=True) ],
			[sg.Text("  details from selected columns will be appended to device details along with hostname in visio")],
			[sg.Text("Appended Columns:")],
			[sg.Multiline("", key='appened_cols', autoscroll=True, size=(20,10), disabled=True) ],

			self.under_line(80),
			])

	def show_declaration(self):
		"""declaration tab details display

		Returns:
			sg.Frame: Frame with declaration page
		"""    		
		return sg.Frame(title='Declaration', 
						title_color='red', 
						# size=(500, 4), 
						key='declaration',						
						relief=sg.RELIEF_SUNKEN, 
						layout=[
			self.under_line(80),
			[sg.Multiline(declaration, autoscroll=True, disabled=True, size=(70,20)) ]

			])

	def event_update_element(self, **kwargs):
		"""update an element based on provided kwargs
		"""    		
		for element, update_values in kwargs.items():
			self.w.Element(element).Update(**update_values)

	def event_update_filter(self, i):
		"""event update when a selection of sheet filter is changed.

		Args:
			i (form_inputs): form elements

		Returns:
			None: None
		"""    		
		updates = {
			'filt_col_key': {'disabled': not i['is_sheet_filter']},
			'filt_col_value': {'disabled': not i['is_sheet_filter']},
			'filt_col_add': {'disabled': not i['is_sheet_filter']},
		}
		self.event_update_element(**updates)
		if not i['is_sheet_filter']:
			self.dic['sheet_filters'] = {}
			self.reset_sheet_filter_boxes()
			return
		if not i['data_file']: 
			sg.Popup("Select DataFile First")
			self.event_update_element(is_sheet_filter={'value': False})
			return None
		try:
			df = pd.read_excel(i['data_file'], sheet_name='Cablings')
			cols = list(df.columns)
			excludes = ( i['dev_a'], i['dev_b'], )
		except:
			sg.Popup("Provide correct column name for\n`Cabling sheet name`\nfrom `DataFile`")
			self.event_update_element(is_sheet_filter={'value': False})
			return None
		for _ in excludes:
			cols.remove(_)
		updates ={ 'filt_col_key': {'values': cols, 'disabled': False}}
		self.event_update_element(**updates)


	def sheet_filter_add_col_value(self, i):
		"""add filter column names to drop boxes when sheet filter is enabled

		Args:
			i (form_inputs): form elements
		"""    		
		if not self.dic['sheet_filters'].get(i['filt_col_key']):
			self.dic['sheet_filters'][i['filt_col_key']] = []	
		self.dic['sheet_filters'][i['filt_col_key']].append(i['filt_col_value'])
		self.reset_sheet_filter_boxes()

	def reset_sheet_filter_boxes(self):
		"""reset the necessary subordinate fieds when sheet filter is disabled.
		"""    		
		mfc = "\n".join([k + "_" + _ +": "+ _ for k, v in self.dic['sheet_filters'].items() for _ in v ])
		updates ={
			'filt_col_key': {'value': ""},
			'filt_col_value': {'value': ""},
			'merged_filt_cols': {'value': mfc}
		}
		self.event_update_element(**updates)

	def update_default_stencil(self, i):
		"""update default stencil parameter when stencil file is selected.

		Args:
			i (form_inputs): form elements
		"""    		
		self.dic['default_stencil'] = ".".join(i['def_stn'].split("/")[-1].split(".")[:-1])

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

	def update_description_col_dropbox(self, i):
		"""dynamic method to different columns dropbox update

		Args:
			i (form_inputs): form elements

		Returns:
			None: None
		"""    	
		if not i['data_file']: 
			sg.Popup("Select DataFile First")
			self.event_update_element(enable_description_merge={'value': False})
			return None
		if i['enable_description_merge']:
			try:
				df = pd.read_excel(i['data_file'], sheet_name='Devices')
				cols = list(df.columns)
				excludes = ('hostname', i['x'], i['y'], )
			except:
				sg.Popup("Provide correct column name for\n`Device sheet name`\nfrom `DataFile`")
				self.event_update_element(enable_description_merge={'value': False})
				return None
			for _ in excludes:
				cols.remove(_)
			updates ={ 'select_col': {'values': cols, 'disabled': False}}
			self.event_update_element(**updates)
			updates = { 'desc_col_add': {'disabled': False} }
			self.event_update_element(**updates)
		else:
			updates ={ 'select_col': {'values': [], 'disabled': True}}
			self.event_update_element(**updates)
			updates = { 'desc_col_add': {'disabled': True} }
			self.event_update_element(**updates)
			self.dic['cols_to_merge'] = []
			updates = { 'appened_cols': {'value': "" }}
			self.event_update_element(**updates)


	def update_col_name(self, field, cols, value):
		"""update an element/field with provided list[cols] and select value

		Args:
			field (str): element
			cols (list): list of items
			value (str): selected item
		"""    	
		updates ={ field: {'values': cols, 'value': value, 'disabled': False} }
		self.event_update_element(**updates)

	def get_value(self, field, cols):
		"""dynamically detect value for the field/element

		Args:
			field (str): element
			cols (list): list of items

		Returns:
			str: detected column name
		"""    		
		value = self.dic[field] 
		if self.dic[field] not in cols:
			value = ""
			for c in cols:
				if c.startswith(self.dic[field][0]):
					value = c
					break
		return value

	def update_devices_cols_combo(self, cols):
		"""update fields/elements for devices tab

		Args:
			cols (list): list of items
		"""    		
		fields = ('x', 'y', )
		for field in fields:
			value = self.get_value(field, cols)
			self.update_col_name(field, cols, value)

	def update_cabling_cols_combo(self, cols):
		"""update fields/elements for cablings tab

		Args:
			cols (list): list of items
		"""    		
		fields = ('dev_a', 'dev_b', )
		for field in fields:
			value = self.get_value(field, cols)
			self.update_col_name(field, cols, value)

	def update_devices_sheet_columns(self, i):
		"""try updating devices tab related fields

		Args:
			i (form_inputs): form elements
		"""    		
		try:
			data_df = pd.read_excel(i['data_file'], sheet_name='Devices')
			data_cols = list(data_df.columns)
			data_cols.remove('hostname')
			self.update_devices_cols_combo(data_cols)
		except:
			sg.Popup("Provide correct `correct device sheet name` and/or `DataFile`")

	def update_cabling_sheet_columns(self, i):
		"""try updating cablings tab related columns

		Args:
			i (form_inputs): form elements
		"""    		
		try:
			cable_df = pd.read_excel(i['data_file'], sheet_name='Cablings')
			cable_cols = list(cable_df.columns)
			self.update_cabling_cols_combo(cable_cols)
		except:
			sg.Popup("Provide correct `correct cabling sheet name` and/or `DataFile`")

	def check_basics(self, i):
		"""pre check after selecting the data file.

		Args:
			i (form_inputs): form elements

		Returns:
			bool: to detect validity of datafile
		"""    		
		if not i['data_file'] :
			sg.Popup("Provide mandatory fields `datafile`, `stencil folder`")
			return False
		return True



# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
	# Test UI #
	# u = UserForm()
	# pprint(u.dic)
	# del(u)
# ------------------------------------------------------------------------------
