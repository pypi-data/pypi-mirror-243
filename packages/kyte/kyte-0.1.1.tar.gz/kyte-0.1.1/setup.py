from setuptools import setup, find_packages

VERSION = '0.1.1'
DESCRIPTION = 'Python module for interfacing Kyte API'
LONG_DESCRIPTION = 'The Kyte API Python Library is designed to facilitate communication between a Python client and the Kyte API endpoint. It simplifies the process of authentication, request signing, and making API calls.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="kyte", 
        version=VERSION,
        author="Kenneth P. Hough",
        author_email="<kenneth@keyqcloud.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(include=['kyte']),
        install_requires=['requests'],
        url="https://github.com/keyqcloud/kyte-api-python",
        license="MIT",
        keywords=['python', 'kyte', 'kyte api'],
        classifiers= [
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ]
)