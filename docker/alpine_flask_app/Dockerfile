FROM alpine:edge
ADD . /alpine
WORKDIR /alpine
RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
&& pip install -r requirements.txt \
&& rm -rf install /var/cache/apk/*

## you make need to update your dns server