__doc__ = '''Networking Tool Set Common Functions
'''


__all__ = [
	# .gpl
	'Default', 'Container', 'Numeric', 'DifferenceDict', 
	'STR', 'IO', 'LST', 'DIC', 'LOG', 'DB', 'IP', 'XL_READ', 'XL_WRITE', 
	'DictMethods', 'Multi_Execution', 'nslookup', 'standardize_if', 'get_username', 'get_password', 
	'get_juniper_int_type', 'get_cisco_int_type', 'get_device_manu',

	# common
	"remove_domain", "read_file", "get_op", "get_ops", "blank_line", "get_device_manufacturar", "verifid_output", 
	"get_string_part", "get_string_trailing", "standardize_mac", "mac_2digit_separated", "mac_4digit_separated", 
	"flatten", "dataframe_generate",

]




from .gpl import (Default, Container, Numeric, 
	DifferenceDict, DictMethods, DIC,
	STR, IO, LST, LOG, DB, IP, XL_READ, XL_WRITE, 
	Multi_Execution, nslookup, standardize_if,
	get_username, get_password, 
	get_juniper_int_type, get_cisco_int_type, get_device_manu
	)
from .common import (
	remove_domain, read_file, get_op, get_ops, blank_line, get_device_manufacturar, verifid_output, 
	get_string_part, get_string_trailing, standardize_mac, mac_2digit_separated, mac_4digit_separated,
	flatten, dataframe_generate
	)


