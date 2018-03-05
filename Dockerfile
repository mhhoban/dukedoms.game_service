FROM python:3.6
ARG wheel
COPY ./dist/$wheel ./$wheel
ARG wheel
RUN pip install $wheel
