
Sumo-Interface
==================

Structure
---------

Sphinx and ReST is used to write the documentation. All source files are in the folder source. The structure of the documentation is:

* source/install - the installation guide

* source/api - API documentation

* source/sumo_interface.rst - documentation master file

* source/conf.py - the sphinx configuration

* source/img - the logo of commonroad project

Dependency installation:

'''
pip install -r requirements_doc.txt
'''

To build the documentation, execute:

'''
make html
'''

and the documentation will be generated in build/html/index.html
