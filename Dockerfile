FROM nikolaik/python-nodejs:python3.10-nodejs17

ARG USERNAME=plenkton
ARG USER_UID=1234
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

RUN sudo apt-get update -y && sudo apt-get install vim -y
RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

ENV POETRY_VIRTUALENVS_CREATE=false

RUN mkdir /code
WORKDIR /code

COPY pyproject.toml poetry.lock /code/
RUN cd /code; poetry install --no-interaction --no-ansi

RUN mkdir /code/front
COPY front/.yarn /code/front/.yarn
COPY front/package.json front/yarn.lock front/.yarnrc.yml front/node_modules /code/front/
RUN yarn set version berry
RUN cd /code/front; yarn install

COPY . /code

USER $USERNAME
