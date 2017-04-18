import os
from setuptools import setup, find_packages
import pygs

# from pygs.examples import available

#Grab the README.md for the long description
long_description = ""

VERSION = pygs.__version__

def setup_package():
    examples = set()
    # for i in available():
    #     if not os.path.isdir('plio/examples/' + i):
    #         if '.' in i:
    #             glob_name = 'examples/*.' + i.split('.')[-1]
    #         else:
    #             glob_name = 'examples/' + i
    #     else:
    #         glob_name = 'examples/' + i + '/*'
    #     examples.add(glob_name)

    setup(
        name = "pygs",
        version = VERSION,
        author = "Kelvin Rodriguez",
        author_email = "kr788@nau.edu",
        description = ("I/O API to support planetary data formats on geoserver."),
        long_description = long_description,
        license = "Public Domain",
        keywords = "planetary io geoserver mongodb",
        url = "http://packages.python.org/pygs",
        packages=find_packages(),
        include_package_data=True,
        package_data={'pygs' : list(examples)},
        zip_safe=False,
        install_requires=[
            'pandas',
            'pyyaml',
            'plio',
            'cyvlfeat',
            'pillow',
            'pysal',
            'scipy',
            'networkx',
            'numexpr',
            'dill',
            'cython',
            'pymongo',
            'datashader',
            'matplotlib'],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Utilities",
            "License :: Public Domain",
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
        ],
    )

if __name__ == '__main__':
    setup_package()
