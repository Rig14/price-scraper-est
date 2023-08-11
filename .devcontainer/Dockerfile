FROM mcr.microsoft.com/devcontainers/base:ubuntu

RUN apt update && apt install -y python3 python3-pip

COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install -r /tmp/requirements-dev.txt && \
    rm /tmp/requirements-dev.txt