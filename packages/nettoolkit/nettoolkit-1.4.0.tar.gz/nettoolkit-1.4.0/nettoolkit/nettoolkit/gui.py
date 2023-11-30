
# ---------------------------------------------------------------------------------------
import PySimpleGUI as sg

import nettoolkit as nt
#
from .forms.gui_template import GuiTemplate
from .forms.tab_event_funcs import TAB_EVENT_UPDATERS
from .forms.formitems import *
from .forms.var_frames import *
from .forms.var_event_funcs import *
from .forms.var_event_updators import *
from .forms.var_retractables import *
#
from nettoolkit.addressing.forms.subnet_scanner import count_ips
# ---------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Class to initiate UserForm
# -----------------------------------------------------------------------------

class Nettoolkit(GuiTemplate):
	'''Minitools UserForm asking user inputs.	'''

	# Object Initializer
	def __init__(self):
		self.header = f'Nettoolkit: {nt.version()} - {super().header}'
		super().__init__()
		self.initialize_variables()
		self.set_button_pallete()

	def initialize_variables(self):
		self.tabs_dic.update(MINITOOLS_FRAMES)
		self.tabs_dic.update(IPSCANNER_FRAMES)
		self.tabs_dic.update(CAPTUREIT_FRAMES)
		self.tabs_dic.update(FACTSFINDER_FRAMES)
		self.tabs_dic.update(J2CONFIG_FRAMES)
		self.tabs_dic.update(PYVIG_FRAMES)
		#
		self.event_catchers.update(MINITOOLS_EVENT_FUNCS)
		self.event_catchers.update(IPSCANNER_EVENT_FUNCS)
		self.event_catchers.update(CATPUREIT_EVENT_FUNCS)
		self.event_catchers.update(FACTSFINDER_EVENT_FUNCS)
		self.event_catchers.update(J2CONFIG_EVENT_FUNCS)
		self.event_catchers.update(PYVIG_EVENT_FUNCS)
		#
		self.event_updaters = self.event_updaters.union(MINITOOLS_EVENT_UPDATERS)
		self.event_updaters = self.event_updaters.union(IPSCANNER_EVENT_UPDATERS)
		self.event_updaters = self.event_updaters.union(CAPTUREIT_EVENT_UPDATERS)
		self.event_updaters = self.event_updaters.union(FACTSFINDER_EVENT_UPDATERS)
		self.event_updaters = self.event_updaters.union(J2CONFIG_EVENT_UPDATERS)
		self.event_updaters = self.event_updaters.union(PYVIG_EVENT_UPDATERS)
		#
		self.tab_updaters = self.tab_updaters.union(TAB_EVENT_UPDATERS)
		#
		self.retractables = self.retractables.union(MINITOOLS_RETRACTABLES)
		self.retractables = self.retractables.union(IPSCANNER_RETRACTABLES)
		self.retractables = self.retractables.union(CAPTUREIT_RETRACTABLES)
		self.retractables = self.retractables.union(FACTSFINDER_RETRACTABLES)
		self.retractables = self.retractables.union(J2CONFIG_RETRACTABLES)
		self.retractables = self.retractables.union(PYVIG_RETRACTABLES)
		#
		self.custom_dynamic_cmd_class = None      # custom dynamic commands execution class
		self.custom_ff_class = None  # custom facts-finder class
		self.custom_fk = {}          # custom facts-finder foreign keys

	def user_events(self, i, event):
		if event == 'file_md5_hash_check':
			self.event_update_element(file_md5_hash_value={'value': ""})
		if event == 'go_count_ips':
			self.event_update_element(ss_ip_counts={'value': count_ips(i['pfxs'], i['till'])})

	@property
	def cleanup_fields(self):
		return self.retractables

	def set_button_pallete(self):
		nbpb = [
			sg.Button("Minitools", change_submits=True, key='btn_minitools'), 
			sg.Button("Addressing", change_submits=True, key='btn_ipscanner'), 
			sg.Button("Capture-IT", change_submits=True, key='btn_captureit'), 
			sg.Button("Facts Gen", change_submits=True, key='btn_factsfinder'), 
			sg.Button("Config Gen", change_submits=True, key='btn_j2config'), 
			sg.Button("Drawing Gen", change_submits=True, key='btn_pyvig'), 
		]
		self.add_to_button_pallete_buttons(nbpb)


# ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- 



# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
	# Test UI #
	# u = Nettoolkit()
	# u()
	# del(u)

# ------------------------------------------------------------------------------
