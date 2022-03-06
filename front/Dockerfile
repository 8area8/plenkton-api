FROM node

RUN mkdir /code
WORKDIR /code

COPY package.json yarn.lock /code/
RUN yarn install
RUN yarn global add @vue/cli

COPY . /code
