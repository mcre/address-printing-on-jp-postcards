FROM paperist/alpine-texlive-ja:2020

WORKDIR /workdir

RUN \
    apk update && \
    apk add python3 py3-pip && \
    pip3 install jaconv
