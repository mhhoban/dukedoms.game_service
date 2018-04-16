from setuptools import setup, find_packages

setup(
  name='dukedomsgameservice',
  version='0.0.0',
  description='microservice for managing game creation and state for Dukedoms of Daleria',
  packages=find_packages(exclude=['swagger_codegen', '&.tests']),
  include_package_data=True,
  install_requires=[
    'addict',
    'connexion',
    'flask',
    'flask_api',
    'psycopg2',
    'retrying',
    'sqlalchemy'
    ]
)
