

# ---------------------------------------------------------------------------------------
#  sets of retractable variables 
# ---------------------------------------------------------------------------------------

MINITOOLS_RETRACTABLES = {
	'file_md5_hash_check', 'file_md5_hash_value',
	'pw_result_juniper', 'pw_result_cisco', 'pw_cisco', 'pw_juniper',
	'file_juniper', 'op_folder_juniper',
}
IPSCANNER_RETRACTABLES = {
	'op_folder', 'pfxs', 'sockets', 'till', 
	'file1', 'file2',
	'op_folder_create_batch', 'pfxs_create_batch', 'names_create_batch', 'ips_create_batch',
	'pfxs_summary_input', 'pfxs_summary_result', 'pfxs_subnet', 'pfxs_supernet', 'pfxs_issubset_result', 
	'pfxs_subnet1', 'pfxs_pieces', 'pfxs_pieces_result',
}
CAPTUREIT_RETRACTABLES = {
	'cit_op_folder', 'cred_en', 'cred_un', 'cred_pw', 
	'device_ip_list_file', 'device_ips',
	'cisco_cmd_list_file', 'cisco_cmds',
	'juniper_cmd_list_file', 'juniper_cmds',
	'custom_cit_file', 'custom_dynamic_cmd_class_name', 'custom_dynamic_cmd_class_str', 'custom_dynamic_cmd_class_depenedt_str',
	'custom_ff_file_cit', 'custom_ff_class_name_cit', 'custom_ff_class_str_cit',
	'custom_fk_file_cit', 'custom_fk_name_cit','custom_fk_str_cit',
	'append_to', 'common_log_file', 'cred_log_type', 'max_connections', 'visual_progress',
}
FACTSFINDER_RETRACTABLES = {
	'ff_log_files', 	
	'custom_ff_file', 'custom_ff_class_name', 'custom_ff_class_str_cit',
	'custom_fk_file', 'custom_fk_name','custom_fk_str_cit',
}
J2CONFIG_RETRACTABLES = set()
PYVIG_RETRACTABLES = {
	'py_stencil_folder', 'py_default_stencil', 'py_output_folder', 'py_op_file', 'pv_input_data_files', 'pv_cm_file', 
}
