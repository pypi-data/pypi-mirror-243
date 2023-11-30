from setuptools import setup, find_packages

import glob

setup(
        name              = 'rk_extractor',
        version           = '0.2.7',
        description       = 'Used to extract RK from simultaneous fits',
        scripts           = glob.glob('scripts/jobs/*') + glob.glob('scripts/offline/*'),
        long_description  = '',
        package_dir       = {'' : 'src'},
        packages          = [''],
        install_requires  = open('requirements.txt').read().splitlines()
        )

