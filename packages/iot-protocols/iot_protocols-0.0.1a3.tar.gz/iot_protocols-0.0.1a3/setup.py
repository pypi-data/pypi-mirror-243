from setuptools import setup, find_packages

VERSION = '0.0.1-a3' 
DESCRIPTION = 'Generic IIoT protocols package'
LONG_DESCRIPTION = 'Package that contains generic interfaced protocols for the IIoT world.'
AUTHOR = "Delhaye Adrien"
MAIL = "adrien.delhaye@memoco.eu"

# Setting up
setup(
        name="iot_protocols", 
        version=VERSION,
        author=AUTHOR,
        author_email=MAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages needed. 
        keywords=['python', 'iiot', 'protocols'],
        classifiers= [
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3.7",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
        ]
)