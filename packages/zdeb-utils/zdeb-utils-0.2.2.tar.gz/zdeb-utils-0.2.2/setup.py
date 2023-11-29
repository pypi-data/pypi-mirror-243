from setuptools import setup

with open("README.md","r") as fd:
    long_description = fd.read()

with open('VERSION', 'r') as vr:
    version = vr.readline().strip()

setup(
    name='zdeb-utils',
    version=version,
    description='Helper to upload and download files to / from Gitlab, as generic packages.',
    author_email='it-support@zilogic.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['zdeb_utils'],
    entry_points={
        'console_scripts': ['zdeb-utils = zdeb_utils.main:main'],
    },
    install_requires=['python-gitlab', 'packaging']
)
