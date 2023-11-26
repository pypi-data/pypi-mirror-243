from setuptools import setup, find_packages

setup(
    name='MeMu',
    version='2.0.9',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"MeMu": ["*.ico", "*.png", "*.ttf"]},
    install_requires=[
        'customtkinter>=5.1.3',
        'Pillow>=9.4.0',
        'pyboy>=1.6.6'
    ],
)