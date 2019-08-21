#!/usr/bin/env python
import sys

import click

from project_info.ecs_utils import deploy_new_task as deploy_new_task_func
from project_info.ecs_utils import stop_service as stop_service_func


@click.group()
def cli():
    pass


@cli.command()
@click.argument('cluster', type=str)
@click.argument('service', type=str)
@click.argument('task_name', type=str)
@click.argument('image', type=str)
def deploy_new_task(cluster, service, task_name, image):
    """Deploy new task in AWS ECS.

    CLUSTER is name of the ecs cluster

    SERVICE is name of the ecs service

    TASK_NAME is name of the ecs service task

    IMAGE is tag of the docker image that should be used
    """
    click.echo(deploy_new_task_func(cluster, service, task_name, image))


@cli.command()
@click.argument('cluster', type=str)
@click.argument('service', type=str)
@click.argument('region', type=str)
def stop_service(cluster, service, region):
    """Stop an AWS ECS service by updating its size and settings it to 0.

    CLUSTER is name of the ecs cluster

    SERVICE is name of the ecs service
    """
    click.echo(stop_service_func(cluster, service, region))


if __name__ == '__main__':
    cli()
