import pathlib
from omegaconf import OmegaConf

if(not 'PROXY_HOST' in globals()): PROXY_HOST = None
if(not 'PROXY_PORT' in globals()): PROXY_PORT = None
_SETTINGS_PATH = pathlib.Path.home() / '.atomica' / 'config.yml'
try:
    config = OmegaConf.load(_SETTINGS_PATH)
    config_core = config.get('core', {})
except FileNotFoundError:
    import warnings
    warnings.warn("~/.atomica/config.yml file is missing or corrupted (ignore this warning if you are running configure.)", UserWarning)
    config_core = {}
    # raise FileNotFoundError('~/.atomica/config.yml file is missing or corrupted. You may want to reinstall the package to fix it.')
