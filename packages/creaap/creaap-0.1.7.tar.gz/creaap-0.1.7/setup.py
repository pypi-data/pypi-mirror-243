from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
   name='creaap',
   version='0.1.7',
   description='CREA Applications in Python toolkit. A bundle of tools to speed up the deelopment of new Python applications in Azure. Allows you to abstract a little over persistence and to manage spatial data.',
   author='CREA',
   author_email='dario.denart@crea.gov.it',
   packages=['creaap', 'creaap.spatial', 'creaap.storage', 'creaap.users'],
   classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
   install_requires=['azure-storage-blob','azure-storage-file-share','azure-data-tables','Shapely>=2.0.0','pytz','pygeoif',
                     'numpy','scipy','scikit-learn','numpy','pyshp','pandas','pyproj', 'msal'], #external packages as dependencies
   include_package_data=True, # to be able to access data files
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://dev.azure.com/dariodenart/_git/CREA%20Application%20Python%20toolkit"
)