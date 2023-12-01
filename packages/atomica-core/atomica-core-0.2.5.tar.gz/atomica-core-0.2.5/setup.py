from setuptools import setup, find_namespace_packages
from setuptools.command.egg_info import egg_info
from setuptools.command.install import install

import sys, pathlib

if '__file__' in globals():
    # we do not want to import atm.core._config_sample as it would include __init__.py
    # which itself requires that the configuration is already written
    atm_core_path = str(pathlib.Path(__file__).parent / 'atomicasoft' / 'core')
    sys.path.insert(0, atm_core_path)
    from configure import config_sample, refresh_settings_file

class egg_info_ex(egg_info):
    """Includes license file into `.egg-info` folder."""

    def run(self):
        # don't duplicate license into `.egg-info` when building a distribution
        if not self.distribution.have_run.get('install', True):
            # `install` command is in progress, copy license
            self.mkpath(self.egg_info)
            self.copy_file('LICENSE', self.egg_info)

        egg_info.run(self)

class PostInstallCommand(install):
    def run(self):
        # Call the original install.run() to perform the default installation
        install.run(self)

        # Run the custom function after installation
        print("Creating/updating the settings file...")
        refresh_settings_file(config_sample=config_sample)


setup(
    name             = 'atomica-core',
    version          = "0.2.5",
    setup_requires = ['omegaconf>=2.3',
                     ],
    install_requires = ['dill>=0.3.6',
                        'xmltodict>=0.13.0',
                        'omegaconf>=2.3',
                       ],
    author           = 'Alexander Shapeev',
    author_email     = 'shapeev@gmail.com',
    license_files    = ('LICENSE',),
    cmdclass         = {'egg_info': egg_info_ex, 'install': PostInstallCommand},
    packages         = find_namespace_packages(include=['atomicasoft.*']),
    zip_safe         = False
)
