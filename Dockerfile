#base image
FROM python:3.10

# setting work directory
WORKDIR /usr/src/app


# env variables
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1


# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        tk\
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# install dependencies
RUN pip install --upgrade pip pipenv 
COPY Pipfile* ./
RUN pipenv install --system --ignore-pipfile

COPY . .

