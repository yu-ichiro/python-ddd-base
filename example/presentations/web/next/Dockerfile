FROM node:slim

WORKDIR /app

# 環境が変わった時のみビルドするレイヤー
COPY ./package.json /app/package.json
COPY ./yarn.lock /app/yarn.lock
RUN yarn install

# ソースコード全体をコピー
COPY . /app

RUN yarn build
CMD yarn start