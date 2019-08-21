#!/usr/bin/env python
import sys
import argparse

import click

from project_info.bitbucket_utils import create_merge_release_pull_request as create_merge_release_pull_request_func


@click.group()
def cli():
    pass


@cli.command()
@click.option('--username', help='username', type=str)
@click.option('--password', help='password', type=str)
@click.option('--source_branch_name', help='source git branch name', type=str)
@click.option('--destination_branch_name', help='destination git branch name', type=str)
@click.option('--repository_name', help='git repository name', type=str)
def create_merge_release_pull_request(username, password, source_branch_name, destination_branch_name, repository_name):
    create_merge_release_pull_request_func(
        username, password, source_branch_name, destination_branch_name, repository_name
    )


if __name__ == '__main__':
    cli()
