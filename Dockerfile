FROM python:3.10

RUN pip3 install poetry

ENV POETRY_VIRTUALENVS_CREATE=false

RUN mkdir /code
WORKDIR /code

COPY pyproject.toml poetry.lock /code/
RUN poetry install --no-interaction --no-ansi

COPY . /code
