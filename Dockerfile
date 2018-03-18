FROM python:3.6
ARG wheel
COPY ./dist/$wheel ./$wheel
ARG wheel
RUN pip install $wheel
ENV GAME_SERVICE_SETTINGS=containerconfig.cfg
CMD ["pip", "show", "dukedoms_game_service"]
