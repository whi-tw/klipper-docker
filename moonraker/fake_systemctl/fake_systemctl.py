#!/usr/bin/python3
import click
import docker
from docker.models.containers import Container

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
        return f'{app_name}.service                                        loaded    {"active" if running else "dead"}   {"running" if running else "exited"}  {app_name.title()}'  # noqa: E501
    elif show:
        return (
            f'{"active" if running else "dead"}\n{"running" if running else "exited"}\n'
        )
    else:
        return running


@click.group()
def cli():
    pass


context = dict(
    ignore_unknown_options=True,
    help_option_names=[],
)


@cli.command(context_settings=context)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def list_units(args):
    for service in docker_services:
        print(app_status(service, list=True))


@cli.command(context_settings=context)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def show(args):
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
    except BaseException:
        pass


@cli.command()
@click.argument("app_name")
def start(app_name):
    try:
        container: Container = docker_client.containers.get(app_name)
        container.start()
    except BaseException:
        pass


@cli.command()
@click.argument("app_name")
def restart(app_name):
    try:
        container: Container = docker_client.containers.get(app_name)
        container.restart()
    except BaseException:
        pass


if __name__ == "__main__":
    cli()
