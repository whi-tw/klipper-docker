# syntax=docker/dockerfile:experimental
FROM debian:buster-slim as build

WORKDIR /opt

RUN --mount=type=cache,id=build-apt,sharing=locked,target=/var/cache/apt/  apt update \
    && apt install -y \
    ca-certificates \
    make \
    gcc \
    git \
    libevent-dev \
    libjpeg62-turbo-dev \
    libbsd-dev \
    libgpiod-dev

COPY upstream/pikvm/ustreamer ustreamer

RUN cd ustreamer \
    && make

## Runtime Image
FROM debian:buster-slim as run

RUN --mount=type=cache,id=run-apt,sharing=locked,target=/var/cache/apt/ apt update \
    && apt install -y \
    ca-certificates \
    libevent-2.1 \
    libevent-pthreads-2.1-6 \
    libjpeg62-turbo \
    libbsd0 \
    libgpiod2

WORKDIR /opt
COPY --from=build /opt/ustreamer ./ustreamer

RUN groupadd ustreamer --gid 1000 \
    && useradd ustreamer --uid 1000 --gid ustreamer \
    && usermod ustreamer --append --groups video \
    && chown -R ustreamer:ustreamer /opt/*

## Start ustreamer
USER ustreamer
EXPOSE 8080
ENTRYPOINT [ "/opt/ustreamer/ustreamer"]
CMD ["--host=0.0.0.0", "--port=8080"]
