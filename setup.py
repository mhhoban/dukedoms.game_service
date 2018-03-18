from setuptools import setup

setup(
  name='dukedoms_game_service',
  version='0.1.0',
  description='microservice for managing game creation and state for Dukedoms of Daleria',
  package='dukedoms_game_service',
  install_requires=[
    'addict',
    'connexion',
    'flask',
    'psycopg2',
    'retrying',
    'sqlalchemy'
    ]
)
