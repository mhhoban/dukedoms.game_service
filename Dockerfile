FROM python:3.6
ARG wheel
COPY ./dist/$wheel ./$wheel
ARG wheel
RUN pip3 install $wheel
ENV GAME_SERVICE_SETTINGS=containerconfig.cfg
CMD ["python", "/usr/local/lib/python3.6/site-packages/game_service/game_service_server.py"]
