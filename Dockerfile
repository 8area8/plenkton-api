FROM nikolaik/python-nodejs:python3.10-nodejs17

RUN pip3 install poetry

ENV POETRY_VIRTUALENVS_CREATE=false

RUN mkdir /code
WORKDIR /code

RUN mkdir /code/front
COPY front/package.json front/yarn.lock /code/front/
RUN cd /code/front; yarn install
RUN cd /code/front; yarn global add @vue/cli

COPY pyproject.toml poetry.lock /code/
RUN cd /code; poetry install --no-interaction --no-ansi

COPY . /code
