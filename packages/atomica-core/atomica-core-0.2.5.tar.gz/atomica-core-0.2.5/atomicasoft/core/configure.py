import yaml

config_sample = """\
core:
  node:
    resources_path: '~/.atomica/resources'
    jobfiles_path: '~/.atomica/jobfiles'
    proxy_path: '~/.atomica/proxy'
    jobfiles_read_attempts: 10
    jobfiles_read_timeout: 3
"""
config_sample = yaml.safe_load(config_sample)

def refresh_settings_file(config_sample):
    import pathlib, sys, os, shutil, site
    from omegaconf import OmegaConf, DictConfig

    _SETTINGS_PATH = pathlib.Path.home() / '.atomica'
    _SETTINGS_PATH.mkdir(mode = 0o700, exist_ok = True)

    config = OmegaConf.create(config_sample)

    # we need a function to update a multilevel dict recursively
    def update_dict_recursive(original_dict, update_dict):
        for key, value in update_dict.items():
            if isinstance(value, DictConfig) and key in original_dict and isinstance(original_dict[key], DictConfig):
                update_dict_recursive(original_dict[key], value)
            else:
                original_dict[key] = value

    try:
        new_dict = OmegaConf.load(pathlib.Path(_SETTINGS_PATH / 'config.yml'))
        update_dict_recursive(config, new_dict)
    except:
        pass

    # now convert strings starting with '~/' into the canonical path
    def apply_function_to_dict(data, func):
        if isinstance(data, DictConfig):
            for key, value in data.items():
                if isinstance(value, DictConfig):
                    apply_function_to_dict(value, func)
                else:
                    data[key] = func(value)

    def convert_user_path(input_string: str):
        if isinstance(input_string, str) and input_string.startswith('~/'):
            return str(pathlib.Path(input_string).expanduser())
        return input_string

    apply_function_to_dict(config, convert_user_path)

    def opener(path, flags):
        return os.open(path, flags, 0o600)
    with open(str(_SETTINGS_PATH / 'config.yml'), "w", encoding ="utf-8", opener = opener) as f:
        f.write(OmegaConf.to_yaml(config))

if __name__ == "__main__":
    refresh_settings_file(config_sample=config_sample)
    print("Settings file created/updated")
