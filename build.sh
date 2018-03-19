#!/bin/bash
python3 setup.py bdist_wheel

package_version='0.1.0'
wheel_file="dukedomsgameservice-$package_version-py3-none-any.whl"
docker build --build-arg wheel=$wheel_file --tag 'mhhoban/dukedoms_game_service:latest' .
