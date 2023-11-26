import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'package/README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name="godjango-material-admin",
    version="1.8.7", # Keeping the version since the latest version of the original repo
    license='MIT License',
    packages=find_packages(),
    author="Anton Maistrenko, Esteban Chacon",
    include_package_data=True,
    author_email="esteban@godjango.dev",
    description="Material Design For Django Administration",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/godjangollc/godjango-material-admin",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        'Framework :: Django :: 3.2',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
