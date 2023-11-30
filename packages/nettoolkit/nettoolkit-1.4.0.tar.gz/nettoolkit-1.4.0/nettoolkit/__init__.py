__doc__ = '''Networking Tool Set'''

__version__ = "1.4.0"


def version():
	return __version__

## --- IMPORTS --- ##

# ---------------- nettoolkit-common ---------------- #
from .nettoolkit_common.gpl import (Default, Container, Numeric, 
	DifferenceDict, DictMethods, DIC,
	STR, IO, LST, LOG, DB, IP, XL_READ, XL_WRITE, 
	Multi_Execution, nslookup, standardize_if,
	get_username, get_password, 
	get_juniper_int_type, get_cisco_int_type, get_device_manu
)
from .nettoolkit_common.common import (
	remove_domain, read_file, get_op, get_ops, blank_line, get_device_manufacturar, verifid_output, 
	get_string_part, get_string_trailing, standardize_mac, mac_2digit_separated, mac_4digit_separated,
	flatten, dataframe_generate
)

# ---------------- nettoolkit-db ---------------- #
from .nettoolkit_db.convertdict import ConvDict
from .nettoolkit_db.database import write_to_xl, append_to_xl, read_xl, get_merged_DataFrame_of_file

# ---------------- pyNetCrypt ---------------- #
from .pyNetCrypt.cpw_cracker import decrypt_type7, encrypt_type7, decrypt_file_passwords, mask_file_passwords
from .pyNetCrypt.jpw_cracker import juniper_decrypt, juniper_encrypt, decrypt_doller9_file_passwords, mask_doller9_file_passwords
from .pyNetCrypt.generate import get_md5

# ---------------- pyJuniper ---------------- #
from .pyJuniper.juniper import Juniper, convert_to_set_from_captures
from .pyJuniper.jset import JSet

# ---------------- nettoolkit ---------------- #
from .nettoolkit.gui import Nettoolkit


## --- DECLARATIONS --- ##

__all__ = [

	# ---------------- nettoolkit-common ---------------- #
	# .gpl
	'Default', 'Container', 'Numeric', 'DifferenceDict', 
	'STR', 'IO', 'LST', 'DIC', 'LOG', 'DB', 'IP', 'XL_READ', 'XL_WRITE', 
	'DictMethods', 'Multi_Execution', 'nslookup', 'standardize_if', 'get_username', 'get_password', 
	'get_juniper_int_type', 'get_cisco_int_type', 'get_device_manu',

	# common
	"remove_domain", "read_file", "get_op", "get_ops", "blank_line", "get_device_manufacturar", "verifid_output", 
	"get_string_part", "get_string_trailing", "standardize_mac", "mac_2digit_separated", "mac_4digit_separated", 
	"flatten", "dataframe_generate",
	
	# ---------------- nettoolkit-db ---------------- #
	# .convertdict
	'ConvDict',
	#databse
	"write_to_xl", "append_to_xl", "read_xl", "get_merged_DataFrame_of_file",

	# ---------------- pyNetCrypt ---------------- #
	# cpw_cracker
	'encrypt_type7', 'decrypt_type7', 'decrypt_file_passwords', 'mask_file_passwords',
	# jpw_cracker
	'juniper_decrypt', 'juniper_encrypt', 'decrypt_doller9_file_passwords', 'mask_doller9_file_passwords',
	# generate
	'get_md5',

	# ---------------- pyJuniper ---------------- #
	# .juniper
	'Juniper', 'convert_to_set_from_captures',
	# Jset
	'JSet',

	# ---------------- nettoolkit.gui ---------------- #
	'Nettoolkit',

]
