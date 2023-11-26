from datazets import get as import_example
from anonym.anonym import anonym


__author__ = 'Erdogan Tasksen'
__email__ = 'erdogan.taskesen@minienw.nl'
__version__ = '0.1.0'

# module level doc-string
__doc__ = """
anonym
=====================================================================

anonym is a python library to anonymize your data set.

Examples
--------
>>> # Example 1
>>> filepath=r'./names_per_department.csv'
>>> filepath_fake=r'./names_per_department_fake.csv'
>>> # Load library
>>> from anonym import anonym
>>> # Initialize
>>> model = anonym(language='dutch', verbose='info')
>>> # Import csv data from file
>>> df = model.import_data(filepath, delim=';')
>>> # Anonimyze the data set
>>> df_fake = model.anonymize(df)
>>> # Write to csv
>>> model.to_csv(df_fake, filepath_fake)

Examples
--------
>>> # Example 2
>>> # Load library
>>> from anonym import anonym
>>> # Initialize
>>> model = anonym(language='english', verbose='info')
>>> # Import example data set
>>> df = model.import_example('titanic')
>>> # Anonimyze the data set
>>> df_fake = model.anonymize(df)

References
----------
https://gitlab.com/datainnovatielab/public/anonym

"""
