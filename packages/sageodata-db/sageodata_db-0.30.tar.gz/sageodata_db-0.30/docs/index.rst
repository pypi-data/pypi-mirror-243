#########################################
sageodata_db Python package documentation
#########################################

Hello! This documentation is about the Python package sageodata_db. This package provides 
code to make it easier to access and use data stored in SA Geodata. 

The source code for sageodata_db is kept at `GitHub
<https://github.com/dew-waterscience/sageodata_db>`_ together with an issue tracker and an
archive of all releases. The repository is not accessible to the public, so please contact
`Kent Inverarity <mailto:Kent.Inverarity@sa.gov.au>`_ for access to the code repository.
You will need a free GitHub.com account in order to view this documentation and access
the source code and issue tracker.


.. toctree::
   :caption: Other documentation
   
   Other versions <../index.html#http://>
   Other packages <../../index.html#http://>

.. toctree::
   :maxdepth: 5
   :caption: Contents:

   installation
   predefined-queries
   apidocs

*********
Changelog
*********

Version 0.23 (24/11/2023)
=========================
- Fix #2 - data_available query's salinities field incorrect - was counting only water chem. 
  Now counting salinity samples as well.

Version 0.14
============
- Add pressure fields to water_levels predefined query (#3)
