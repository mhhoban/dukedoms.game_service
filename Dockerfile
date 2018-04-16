FROM python:3.6
ARG game_service_wheel
COPY ./dist/$game_service_wheel /$game_service_wheel
ARG swagger_wheel
COPY ./swagger_codegen/dist/$swagger_wheel /$swagger_wheel

ARG game_service_wheel
RUN pip3 install /$swagger_wheel && pip3 install /$game_service_wheel
ENV GAME_SERVICE_ENV=container
CMD ["python", "/usr/local/lib/python3.6/site-packages/game_service/game_service_server.py"]
