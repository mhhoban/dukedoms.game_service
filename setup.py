from setuptools import setup

setup(
  name='game_service',
  version='0.1.0',
  description='microservice for managing game creation and state for Dukedoms of Daleria',
  package='game_service',
  install_requires=[
    'flask',
    'psycopg2',
    'sqlalchemy'
    ]
)
