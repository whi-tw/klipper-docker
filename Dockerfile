FROM ubuntu:18.04

RUN apt-get update && apt-get install -y sudo

# Create user
RUN useradd -ms /bin/bash -u1001 klippy && usermod -aG dialout,tty klippy
USER klippy

### Klipper setup ###
WORKDIR /home/klippy

COPY upstream/Klipper3d/klipper klipper
COPY ["upstream/EtteGit/EnragedRabbitProject/Klipper_Files/Extra module/ercf.py", "klipper/klippy/extras/"]

USER root
RUN echo 'klippy ALL=(ALL:ALL) NOPASSWD: ALL' >/etc/sudoers.d/klippy && chown klippy:klippy -R klipper
# This is to allow the install script to run without error
RUN ln -s /bin/true /bin/systemctl
USER klippy
RUN ./klipper/scripts/install-ubuntu-18.04.sh
# Clean up install script workaround
RUN sudo rm -f /bin/systemctl

# create volume mountpoints
RUN mkdir /home/klippy/.config /home/klippy/sockets
VOLUME ["/home/klippy/.config", "/home/klippy/sockets"]

ENTRYPOINT ["/home/klippy/klippy-env/bin/python", "/home/klippy/klipper/klippy/klippy.py", "/home/klippy/.config/printer.cfg"]
