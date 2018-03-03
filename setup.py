from setuptools import find_packages, setup

setup(
  name='dukedoms_game_service',
  version='0.1.0',
  description='microservice for managing game creation and state for Dukedoms of Daleria',
  packages=find_packages(exclude=['contrib', 'docs', 'tests'])
)
