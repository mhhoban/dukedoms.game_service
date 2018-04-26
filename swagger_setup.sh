#!/bin/bash
rm -rvf swagger_codegen
curl https://raw.githubusercontent.com/mhhoban/dukedoms.game_service_api/master/dukedoms_game_service_api.yaml -O
mv dukedoms_game_service_api.yaml game_service/swagger/game_service_api.yaml

# fetch other specs
curl https://raw.githubusercontent.com/mhhoban/dukedoms.account_service_spec/master/dukedoms_account_service_api.yaml -O
mv dukedoms_account_service_api.yaml game_service/swagger/account_service_api.yaml

docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate -i \
./local/game_service/swagger/game_service_api.yaml -l python-flask -o /local/swagger_codegen
cd swagger_codegen
python3 setup.py bdist_wheel
cd ..
pip3 install swagger_codegen/dist/swagger_server-1.0.0-py3-none-any.whl
