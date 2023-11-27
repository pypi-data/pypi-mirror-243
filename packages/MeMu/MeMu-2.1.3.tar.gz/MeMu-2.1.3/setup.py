from setuptools import setup, find_packages

setup(
    name='MeMu',
    version='2.1.3',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    Description='This is a user interface for running pyboy emulator. To use,\n import MeMu\nemu=MeMu.Backend()\nemu.turn_on()',
    include_package_data=True,
    package_data={"MeMu": ["*.ico", "*.png"]},
    install_requires=[
        'customtkinter>=5.1.3',
        'Pillow>=9.4.0',
        'pyboy>=1.6.6'
    ],
)