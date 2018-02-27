FROM python:3.5.5-jessie

ADD . /app

RUN apt-get update && apt-get install build-essential libssl-dev -y

RUN mkdir -p /usr/local/nvm

ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 8.5.0
ENV REACT_APP_API_ROOT='mail2.ameo.link'
ENV REACT_APP_API_PORT=4545

WORKDIR /app/frontend

RUN curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default \
    && npm install \
    && npm run build

WORKDIR /app/backend

RUN cp -r /app/frontend/build /app/backend/static

RUN pip install -r requirements.txt

CMD ["python", "entrypoint.py"]
