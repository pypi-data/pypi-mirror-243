from setuptools import setup

setup(
    name='mailguard',
    version='0.1.0.dev0',  # Append '.dev0' to indicate development status
    description='Forensic tool for analyzing email headers',
    author='Mayank Rajput',
    author_email='hackelite.sup@gmail.com',
    packages=['mailguard'],
    install_requires=[
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'mailguard = mailguard:main',
        ],
    },
)
