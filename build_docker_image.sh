#!/bin/bash

python setup.py bdist_wheel

game_service_wheel="dukedomsgameservice-0.0.0-py3-none-any.whl"
swagger_wheel="swagger_server-1.0.0-py3-none-any.whl"

docker build --build-arg game_service_wheel=$game_service_wheel \
  --build-arg swagger_wheel=$swagger_wheel --tag 'mhhoban/dukedoms_game_service:latest' .
