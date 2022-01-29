# syntax=docker/dockerfile:experimental

FROM python:2 as build-venv

WORKDIR /opt

COPY upstream/Klipper3d/klipper klipper
COPY ["upstream/EtteGit/EnragedRabbitProject/Klipper_Files/Extra module/ercf.py", "klipper/klippy/extras/"]
COPY extra_files/gcode_shell_command.py klipper/klippy/extras/

RUN --mount=type=cache,id=venv-wheel,sharing=locked,target=/root/.cache/pip virtualenv -p python2 venv \
    && venv/bin/pip install -r klipper/scripts/klippy-requirements.txt \
    && venv/bin/python -m compileall klipper/klippy \
    && venv/bin/python klipper/klippy/chelper/__init__.py

FROM python:2-slim as run

WORKDIR /opt
COPY --from=build-venv /opt/klipper ./klipper
COPY --from=build-venv /opt/venv ./venv

RUN mkdir run cfg gcode

RUN groupadd klipper --gid 1000 \
    && useradd klipper --uid 1000 --gid klipper \
    && usermod klipper --append --groups dialout \
    && chown -R klipper:klipper /opt/*

USER klipper
VOLUME ["/opt/run", "/opt/cfg", "/opt/gcode", "/opt/log"]
ENTRYPOINT ["/opt/venv/bin/python", "klipper/klippy/klippy.py"]
CMD ["-a", "run/klipper.sock", "-l", "log/klippy.log", "cfg/printer.cfg"]
