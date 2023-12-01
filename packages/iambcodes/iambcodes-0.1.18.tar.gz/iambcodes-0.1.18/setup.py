import setuptools
# getting the latest version from the __init__.py file in src/iambcodes
import re
import os
VERSIONFILE = os.path.join('src', 'iambcodes', '__init__.py')
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__=['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setuptools.setup(
    name='iambcodes',
    version=verstr,
    author='Ulf Liebal',
    author_email='ulf.liebal@rwth-aachen.de',
    description='Functions for data analysis support at the iAMB in RWTH Aachen.',
    keywords='biotechnology',
    url='https://git.rwth-aachen.de/ulf.liebal/iambcodes',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=[
        'xlrd>=2.0.1',
        'numpy>=1.22.0',
        'cobra>=0.22.1',
        'biopython>=1.78',
        'matplotlib>=3.3.4',
        'scipy>=1.9.0',
        'openpyxl>=3.0.9',
        'xlsxwriter>=3.0.1',
    ],
)
