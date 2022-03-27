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

USER $USERNAME
