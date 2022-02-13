ARG PYTHON_VERSION=3.10-slim-bullseye

FROM python:${PYTHON_VERSION} as python

# Python 'dev' stage
FROM python as backend-dev

ARG BUILD_ENVIRONMENT=local

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

ARG APP_HOME=/app

RUN apt-get update && \
  apt-get install --no-install-recommends -y \
  # ca-certificates \
  # curl \
  # netbase \
  # wget \
  # autoconf \
  # automake \
  # bzip2 \
  # dpkg-dev \
  # file \
  # g++ \
  # gcc \
  build-essential \
  # imagemagick \
  # libbz2-dev \
  # libc6-dev \
  # libcurl4-openssl-dev \
  # libdb-dev \
  # libevent-dev \
  libffi-dev \
  # libgdbm-dev \
  # libglib2.0-dev \
  # libgmp-dev \
  # libjpeg-dev \
  # libkrb5-dev \
  # liblzma-dev \
  # libmagickcore-dev \
  # libmagickwand-dev \
  # libmaxminddb-dev \
  # libncurses5-dev \
  # libncursesw5-dev \
  # libpng-dev \
  libpq-dev \
  # libreadline-dev \
  # libsqlite3-dev \
  libssl-dev \
  # libtool \
  # libwebp-dev \
  # libxml2-dev \
  # libxslt-dev \
  # libyaml-dev \
  # musl-dev \
  # make \
  # patch \
  # unzip \
  # xz-utils \
  # zlib1g-dev \
  # $(if apt-cache show 'default-libmysqlclient-dev' 2>/dev/null | grep -q '^Version:'; then \
  #     echo 'default-libmysqlclient-dev'; \
  # else \
  #     echo 'libmysqlclient-dev'; \
  # fi);  \
  # # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY ./requirements .

RUN pip install --no-cache-dir --no-index  \ 
  --upgrade pip setuptools wheel 

RUN pip wheel --wheel-dir /usr/src/app/wheels  \
  -r ${BUILD_ENVIRONMENT}.txt

RUN pip install  \
  --no-cache-dir  \
  --no-index  \
  --find-links=/usr/src/app/wheels  \
  /usr/src/app/wheels/*  \
  && rm -rf /usr/src/app/wheels

WORKDIR ${APP_HOME}

COPY ./compose/production/backend/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/backend/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./src ${APP_HOME}

ENTRYPOINT [ "/entrypoint" ]