

# ---------------------------------------------------------------------------------------
from .var_frames import MINITOOLS_FRAMES, IPSCANNER_FRAMES, CAPTUREIT_FRAMES, FACTSFINDER_FRAMES, J2CONFIG_FRAMES, PYVIG_FRAMES

# ---------------------------------------------------------------------------------------
TAB_EVENT_UPDATERS = { 	'btn_ipscanner', 
						'btn_minitools', 
						'btn_captureit', 
						'btn_factsfinder', 
						'btn_j2config',
						'btn_pyvig',
}
#
# ---------------------------------------------------------------------------------------
ALL_TABS = set()
ALL_TABS = ALL_TABS.union(IPSCANNER_FRAMES.keys())
ALL_TABS = ALL_TABS.union(MINITOOLS_FRAMES.keys())
ALL_TABS = ALL_TABS.union(CAPTUREIT_FRAMES.keys())
ALL_TABS = ALL_TABS.union(FACTSFINDER_FRAMES.keys())
ALL_TABS = ALL_TABS.union(J2CONFIG_FRAMES.keys())
ALL_TABS = ALL_TABS.union(PYVIG_FRAMES.keys())

# ---------------------------------------------------------------------------------------

def enable_disable(obj, tabs_to_enable, button=set()):
	"""enable/disable provided object frames

	Args:
		obj (Nettoolkit): Nettoolkit class instance object
		tabs_to_enable (list): list of tabs to be enabled
	"""	
	tabs_to_disable = ALL_TABS.difference(tabs_to_enable)
	buttons_to_rev = TAB_EVENT_UPDATERS.difference(button)
	for tab in tabs_to_disable:
		d = {tab: {'visible':False}}
		obj.event_update_element(**d)	
	for i, tab in enumerate(tabs_to_enable):
		e = {tab: {'visible':True}}
		obj.event_update_element(**e)
		if i ==0: obj.w[tab].select()
	if button:
		for tab in buttons_to_rev:
			e = {tab: {'button_color': 'gray'}}
			obj.event_update_element(**e)
		e = {button: {'button_color': 'blue'}}
		obj.event_update_element(**e)



# ---------------------------------------------------------------------------------------
#  ADD / EDIT FRAMES UPDATE HERE
#

def btn_ipscanner_exec(obj):
	"""executor function to switch and enable ipscanner tabs

	Args:
		obj (Nettoolkit): Nettoolkit class instance object

	Returns:
		True: when succeded
	"""	
	enable_disable(obj, IPSCANNER_FRAMES.keys(), button='btn_ipscanner')
	return True

def btn_minitools_exec(obj):
	"""executor function to switch and enable minitools tabs

	Args:
		obj (Nettoolkit): Nettoolkit class instance object

	Returns:
		True: when succeded
	"""	
	enable_disable(obj, MINITOOLS_FRAMES.keys(), button='btn_minitools')
	return True

def btn_captureit_exec(obj):
	"""executor function to switch and enable captureit tabs

	Args:
		obj (Nettoolkit): Nettoolkit class instance object

	Returns:
		True: when succeded
	"""	
	enable_disable(obj, CAPTUREIT_FRAMES.keys(), button='btn_captureit')
	return True

def btn_factsfinder_exec(obj):
	"""executor function to switch and enable factsfinder tabs

	Args:
		obj (Nettoolkit): Nettoolkit class instance object

	Returns:
		True: when succeded
	"""	
	enable_disable(obj, FACTSFINDER_FRAMES.keys(), button='btn_factsfinder')
	return True

def btn_j2config_exec(obj):
	"""executor function to switch and enable j2config tabs

	Args:
		obj (Nettoolkit): Nettoolkit class instance object

	Returns:
		True: when succeded
	"""	
	enable_disable(obj, J2CONFIG_FRAMES.keys(), button='btn_j2config')
	return True

def btn_pyvig_exec(obj):
	"""executor function to switch and enable pyvig tabs

	Args:
		obj (Nettoolkit): Nettoolkit class instance object

	Returns:
		True: when succeded
	"""	
	enable_disable(obj, PYVIG_FRAMES.keys(), button='btn_pyvig')
	return True

# ---------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ------------------------------------------------------------------------------
