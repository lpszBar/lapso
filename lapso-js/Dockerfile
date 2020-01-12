FROM node:13-stretch-slim
COPY . /app
WORKDIR /app

RUN npm build

ENTRYPOINT  ["npm"]
CMD ["start" "--host" "0.0.0.0" ]