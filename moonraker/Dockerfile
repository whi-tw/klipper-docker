# syntax = docker/dockerfile:experimental
FROM python:3.9 as build-venv

WORKDIR /opt

COPY upstream/Arksine/moonraker moonraker

RUN --mount=type=cache,id=venv-wheel,sharing=locked,target=/root/.cache/pip python -m venv venv \
    && venv/bin/pip install -r moonraker/scripts/moonraker-requirements.txt

FROM python:3.9 as build-fake-systemd-venv

WORKDIR /opt
COPY fake_systemctl fake_systemctl
WORKDIR /opt/fake_systemctl
RUN --mount=type=cache,id=systemctl-wheel,sharing=locked,target=/root/.cache/pip python -m venv venv \
    && venv/bin/pip install -r requirements.txt

FROM python:3.9-slim as run

RUN --mount=type=cache,id=apt,sharing=locked,target=/var/cache/apt/ apt update \
    && apt install -y \
    libopenjp2-7 \
    python3-libgpiod \
    curl \
    libcurl4-openssl-dev \
    libssl-dev \
    liblmdb0 \
    libsodium-dev \
    zlib1g-dev \
    iproute2 \
    sudo

WORKDIR /opt
COPY --from=build-venv /opt/moonraker ./moonraker
COPY --from=build-venv /opt/venv ./venv
COPY --from=build-fake-systemd-venv /opt/fake_systemctl ./fake_systemctl

RUN cp /opt/fake_systemctl/systemctl /bin/ \
    && chmod a+x /bin/systemctl

RUN mkdir run cfg gcode db log
RUN groupadd moonraker --gid 1000 \
    && groupadd gpio --gid 997 \
    && useradd moonraker --uid 1000 --gid moonraker \
    && usermod moonraker --append --groups dialout,gpio \
    && chown -R moonraker:moonraker /opt/* \
    && echo 'moonraker ALL= NOPASSWD: /bin/systemctl *' > /etc/sudoers.d/moonraker \
    && echo 'moonraker ALL= NOPASSWD: /opt/fake_systemctl/venv/bin/python /opt/fake_systemctl/fake_systemctl.py *' >> /etc/sudoers.d/moonraker
## Start Moonraker
USER moonraker
EXPOSE 7125
VOLUME ["/opt/run", "/opt/cfg", "/opt/gcode", "/opt/db", "/opt/log", "/var/run/docker.sock"]
ENTRYPOINT ["/opt/venv/bin/python", "moonraker/moonraker/moonraker.py"]
CMD ["-c", "cfg/moonraker.cfg", "-l", "log/moonraker.log"]
