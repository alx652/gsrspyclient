import yaml

with open("config/app.yaml", "r", encoding="utf-8") as ymlfile:
    config = yaml.full_load(ymlfile)

def check_host_key(option_value):
    # if option_value is not None:
    #    if option_value in gsrs_config.config['host_keys'][option_value]:
    #        return option_value
    # if option_value is None:
    # For now only default_host_key works
    key = "default_host_key"
    if key in config:
        return config[key]
    return None

def get_suppress_sslverify_warning():
    host_key = get_default_host_key()
    return config['host_keys'][host_key]['suppress_sslverify_warning']

def get_auth_username():
    host_key = get_default_host_key()
    return config['host_keys'][host_key]['auth_username']

def get_auth_method():
    host_key = get_default_host_key()
    return config['host_keys'][host_key]['auth_method']

def get_auth_method_value():
    host_key = get_default_host_key()
    return config['host_keys'][host_key]['auth_method_value']

def get_base_url():
    host_key = get_default_host_key()
    return config['host_keys'][host_key]['base_url']

def get_default_host_key():
    return config['default_host_key']
