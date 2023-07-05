from setuptools import setup, find_packages

setup(
    name='jamcoders',
    version='1.0.2',
    author='Jamcoders',
    author_email='jamcoders@jamcoders.com',
    description='Utilities for JamCoders',
    packages=find_packages(),
    install_requires=[
        'termcolor',
    ],
)
