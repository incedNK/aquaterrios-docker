#!/bin/bash

# FROM ubuntu AS builder-image

# ARG DEBIAN_FRONTEND=noninteractive

# RUN apt-get update && apt-get install --no-install-recommends -y python3 python3-dev python3-venv python3-pip python3-wheel build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*

# RUN python3 -m venv /home/fastapi/venv
# ENV PATH="/home/fastapi/venv/bin:$PATH"

# RUN pip3 install --no-cache-dir --upgrade pip

# COPY requirements.txt .
# RUN pip3 install --no-cache-dir -r requirements.txt

# FROM ubuntu AS runner-image
# RUN apt-get update && apt-get install --no-install-recommends -y python3 python3-venv && apt-get clean && rm -rf /var/lib/apt/lists/*

# RUN useradd --create-home fastapi
# COPY --from=builder-image /home/fastapi/venv /home/fastapi/venv

# USER fastapi
# RUN mkdir /home/fastapi/app
# WORKDIR /home/fastapi/app
# COPY . .

# EXPOSE 8000

# ENV PYTHONUNBUFFERED=1

# ENV VIRTUAL_ENV=/home/fastapi/venv
# ENV PATH="/home/fastapi/venv/bin:$PATH"

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade setuptools

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]