from setuptools import setup, find_packages

setup(
    name="mtmtoolkit",
    version="0.0.9-alpha",
    packages=find_packages(),
    description='A convenient tool for chemists or researchers who need to prepare Gaussian input files quickly, without manually converting SMILES to XYZ format or typing out the Gaussian input file parameters by hand. ',
    author='rrau-bsu',
    author_email='ryanrau@u.boisestate.edu',
    license='MIT',
    url='https://github.com/rrau-bsu/MTMToolkit',
    install_requires=[
        "PyQt6",
        "PyQt6-WebEngine",
        "rdkit",
        "flask",
    ],
    entry_points = {
        'console_scripts': [
            'mtmtk=mtmtoolkit.__main__:main',
            
        ],
    },
)
