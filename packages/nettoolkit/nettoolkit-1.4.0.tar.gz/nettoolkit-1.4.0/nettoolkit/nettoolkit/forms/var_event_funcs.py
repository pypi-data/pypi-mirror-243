

# ---------------------------------------------------------------------------------------
#
from .tab_event_funcs import *
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
#   dictionary of event updators v/s its executor functions.
# ---------------------------------------------------------------------------------------

MINITOOLS_EVENT_FUNCS = {
	'go_md5_calculator': md5_calculator_exec,
	'go_pw_enc_cisco': pw_enc_cisco_exec,
	'go_pw_dec_cisco': pw_dec_cisco_exec,
	'go_pw_enc_juniper': pw_enc_juniper_exec,
	'go_pw_dec_juniper': pw_dec_juniper_exec,
	'go_juniper_to_set': juniper_oper_to_jset_exec,
	'go_juniper_remove_remarks': juniper_oper_remove_remarks_exec,
	'go_compare_config_text': go_compare_config_text_exec,
	'go_compare_config_xl': go_compare_config_xl_exec,
}
IPSCANNER_EVENT_FUNCS = {
	'btn_ipscanner': btn_ipscanner_exec,
	'go_subnet_scanner': subnet_scanner_exec,
	'go_compare_scanner_outputs': compare_scanner_outputs_exec,
	'go_create_batch': create_batch_exec,
	'btn_minitools': btn_minitools_exec,
	'go_pfxs_summary': prefixes_oper_summary_exec,
	'go_pfxs_issubset' : prefixes_oper_issubset_exec,
	'go_pfxs_break': prefixes_oper_pieces_exec,
}
CATPUREIT_EVENT_FUNCS = {
	'device_ip_list_file': device_ip_list_file_exec,
	'cisco_cmd_list_file': cisco_cmd_list_file_exec,
	'juniper_cmd_list_file': juniper_cmd_list_file_exec,
	'cit_common': cit_common_exec,
	'custom_cit_file': custom_cit_file_exec,
	'custom_dynamic_cmd_class_name': custom_dynamic_cmd_class_name_exec,
	'custom_ff_file_cit': custom_ff_file_cit_exec,
	'custom_fk_file_cit': custom_fk_file_cit_exec,
	'custom_ff_class_name_cit': custom_ff_name_cit_exec,
	'custom_fk_name_cit': custom_fk_name_cit_exec,
	'btn_captureit': btn_captureit_exec,
}
FACTSFINDER_EVENT_FUNCS = {
	'btn_ff_gen': btn_ff_gen_exec, 
	'btn_factsfinder': btn_factsfinder_exec,
	'custom_ff_file': custom_ff_file_exec,
	'custom_fk_file': custom_fk_file_exec,
	'custom_ff_class_name': custom_ff_name_exec,
	'custom_fk_name': custom_fk_name_exec,
}
J2CONFIG_EVENT_FUNCS = {
	'btn_j2config': btn_j2config_exec,
	'btn_j2_gen': btn_j2_gen_exec,
	'j2_custom_reg': j2_custom_reg_exec,
}
PYVIG_EVENT_FUNCS = {
	'btn_pyvig': btn_pyvig_exec,
	'pv_data_start': pv_data_start_exec,
	'pv_start': pv_start_exec,
}

# ---------------------------------------------------------------------------------------
