FROM paperist/alpine-texlive-ja

WORKDIR /workdir

RUN \
    apk update && \
    apk add python3 && \
    pip3 install jaconv
