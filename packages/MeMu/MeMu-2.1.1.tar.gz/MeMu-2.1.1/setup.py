from setuptools import setup, find_packages

setup(
    name='MeMu',
    version='2.1.1',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"MeMu": ["*.ico", "*.png"]},
    install_requires=[
        'customtkinter>=5.1.3',
        'Pillow>=9.4.0',
        'pyboy>=1.6.6'
    ],
)