

# ---------------------------------------------------------------------------------------
#
from nettoolkit.pyJuniper.forms.md5_calculator import *
from nettoolkit.pyJuniper.forms.pw_enc_dec import *
from nettoolkit.pyJuniper.forms.juniper_oper import *
#
from nettoolkit.addressing.forms.subnet_scanner import *
from nettoolkit.addressing.forms.compare_scanner_outputs import *
from nettoolkit.addressing.forms.prefixes_oper import *
from nettoolkit.addressing.forms.create_batch import *
#
from nettoolkit.capture_it.forms.cred import *
from nettoolkit.capture_it.forms.options import *
from nettoolkit.capture_it.forms.common_to_all import *
from nettoolkit.capture_it.forms.custom import *
#
from nettoolkit.facts_finder.forms.ff_generate import *
from nettoolkit.facts_finder.forms.ff_custom import *
from nettoolkit.facts_finder.forms.ff_custom_cit import *
#
from nettoolkit.pyVig.forms.input_data import *
from nettoolkit.pyVig.forms.custom import *
#
from nettoolkit.j2config.forms.input_data import *
#
from nettoolkit.compare_it.forms.compare_configs import *
#
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
#   Frames - tabs and its frame functions
# ---------------------------------------------------------------------------------------
MINITOOLS_FRAMES = {
	'1.Juniper': juniper_oper_frame(),
	'2.P/W Enc/Dec': pw_enc_decr_frame(),
	'3.MD5 Calculate': md5_calculator_frame(),
	'4.Compare-it': compare_config_texts_frame(),
}
IPSCANNER_FRAMES = {
	'1.Subnet Scanner': subnet_scanner_frame(),
	'2.Scan Compare': compare_scanner_outputs_frame(),
	'3.Create Batch': create_batch_frame(),
	'4.Summarize':summarize_prefixes_frame(),
	'5.Break Prefix':devide_prefixes_frame(),
	'6.isSubset':issubset_check_prefix_frame(),
}
CAPTUREIT_FRAMES = {
	'1.Capture': exec_common_to_all_frame(),
	'2.Cred': exec_cred_frame(),
	'3.Options': exec_options_frame(),
	'4.Customize Capture': exec_custom_frame(),
	'5.Facts Gen': exec_ff_custom_cit_frame(),
}
FACTSFINDER_FRAMES = {
	'1.Facts Gen': btn_ff_gen_frame(),	
	'2.Customize Facts': exec_ff_custom_frame(),
}
J2CONFIG_FRAMES = {
	'1.Config Gen': j2_gen_frame(),
}
PYVIG_FRAMES = {
	'1.pyVig Excel Gen': pv_input_data_frame(),
	'2.Visio Gen': pv_input_visio_frame(),
	'3.Customize pyVig': pv_custom_data_frame(),
}

# ---------------------------------------------------------------------------------------
