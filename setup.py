from setuptools import setup, find_packages

setup(
    name='rakutengenie',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'google-generativeai',
    ],
    entry_points={
        'console_scripts': [
            'rakutengenie=rakutengenie.main:main'
        ],
    },
    
)
