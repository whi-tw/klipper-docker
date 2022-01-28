#!/usr/bin/python3
import subprocess
import sys
import docker
from docker.models.containers import Container
import click


docker_client = docker.from_env()

docker_services = ("moonraker", "klipper")


def app_status(app_name, list=False, show=False):
    running = False
    try:
        container = docker_client.containers.get(app_name)
        if container.status == "running":
            running = True
    except docker.errors.NotFound:
        pass

    if list:
        return f'{app_name}.service                                        loaded    {"active" if running else "dead"}   {"running" if running else "exited"}  {app_name.title()}'
    elif show:
        return (
            f'{"active" if running else "dead"}\n{"running" if running else "exited"}\n'
        )
    else:
        return running


@click.group()
def cli():
    pass


@cli.command()
def list_units():
    for service in docker_services:
        print(app_status(service, list=True))


@cli.command()
def show():
    for service in docker_services:
        print(app_status(service, show=True))


@cli.command()
@click.argument("app_name")
def status(app_name):
    if app_status(app_name):
        print("Running")
    else:
        print("Stopped")


@cli.command()
@click.argument("app_name")
def stop(app_name):
    try:
        container: Container = docker_client.containers.get(app_name)
        container.stop()
    except:
        pass


@cli.command()
@click.argument("app_name")
def start(app_name):
    try:
        container: Container = docker_client.containers.get(app_name)
        container.start()
    except:
        pass


@cli.command()
@click.argument("app_name")
def restart(app_name):
    try:
        container: Container = docker_client.containers.get(app_name)
        container.restart()
    except:
        pass


if __name__ == "__main__":
    cli()
