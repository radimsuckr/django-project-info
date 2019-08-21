#!/usr/bin/env python
import sys
import argparse

import click

from project_info.git_utils import create_release_branch as create_release_branch_func
from project_info.git_utils import create_deployment_branch as create_deployment_branch_func
from project_info.git_utils import checkout_to_release_branch as checkout_to_release_branch_func
from project_info.git_utils import commit_version as commit_version_func
from project_info.git_utils import merge_release_branch as merge_release_branch_func
from project_info.version_utils import get_next_version, get_version
from project_info.types import EnumType, ReleaseType


@click.group()
def cli():
    pass


@cli.command()
@click.option('--release_type', help='release type', type=EnumType(ReleaseType), required=True)
@click.option('--build_hash',  help='hash of the build', type=str)
@click.option('--file',  help='path to the version file', type=str, default='version.json', required=True)
@click.option('--remote_name', help='repository name', type=str)
@click.option('--branch_name', help='branch name', type=str)
def create_release_branch(release_type, build_hash, file, remote_name, branch_name):
    """
    Create relase branch and push it to the remote repository if remote name is specified
    """
    create_release_branch_func(
        get_next_version(release_type, build_hash, file), release_type, remote_name, branch_name
    )


@cli.command()
@click.option('--environment', help='deployment environment', type=str)
def create_deployment_branch(environment):
    create_deployment_branch_func(environment)


@cli.command()
def checkout_to_release_branch():
    checkout_to_release_branch_func()


@cli.command()
@click.option('--version', help='version', type=str)
@click.option('--files',  help='path to the version files', type=list, default=['version.json'])
@click.option('--remote_name', help='repository name', type=str)
def commit_version(version, files, remote_name):
    commit_version_func(version, files, remote_name)


@cli.command()
@click.option('--to_branch_name', help='branch name', type=str, default='next')
@click.option('--remote_name', help='repository name', type=str)
def merge_release_branch(to_branch_name, remote_name):
    merge_release_branch_func(to_branch_name, remote_name)



if __name__ == '__main__':
    cli()
