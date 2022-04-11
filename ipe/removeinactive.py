def get_safe_meta_data(meta_data_name):
    safe_meta = ''
    meta_data_value = document.get_meta_data_value(meta_data_name)
    if meta_data_value:
        safe_meta = meta_data_value[-1]
    return safe_meta

workstatus = get_safe_meta_data('workstatus').lower()

if workstatus == 'inactive':
    log('REJECT: inactive')
    document.reject()