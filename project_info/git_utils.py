import json
import os
import git
import re
import sys

from click import BadParameter, UsageError

from .types import ReleaseType


DEPLOYMENT_COMMIT_PATTERN = r'^Deployment of "(?P<branch_name>.+)"$'


def create_release_branch(version, release_type, remote_name=None, branch_name=None):
    repo = git.Repo(os.getcwd())
    g = repo.git

    if branch_name:
        g.checkout(branch_name)
    if remote_name:
        g.pull(remote_name, branch_name)

    release_branch_name = '{}-{}'.format(release_type, version)
    g.checkout(branch_name or 'HEAD', b=release_branch_name)


def create_deployment_branch(environment, remote_name=None, branch_name=None):
    repo = git.Repo(os.getcwd())
    g = repo.git
    source_branch_name = repo.head.reference
    deployment_branch_name = 'deploy-{}'.format(environment)

    g.checkout('HEAD', b=deployment_branch_name)
    g.commit('--allow-empty', message='Deployment of "{}"'.format(source_branch_name))

    if remote_name:
        g.push(remote_name, deployment_branch_name)


def checkout_to_release_branch(remote_name=None):
    repo = git.Repo(os.getcwd())
    g = repo.git
    match = re.match(DEPLOYMENT_COMMIT_PATTERN, repo.head.commit.message)
    if not match:
        raise UsageError('Invalid deployment branch commit')

    branch_name = match.group('branch_name')
    g.checkout(branch_name)
    if remote_name:
        g.pull(remote_name, branch_name)


def commit_version(version, files=['version.json'], remote_name=None):
    repo = git.Repo(os.getcwd())
    g = repo.git

    g.add(files)
    g.commit(m=str(version))
    g.tag(str(version))

    if remote_name:
        g.push(remote_name, repo.head.reference)
        g.push(remote_name, str(version))


def merge_release_branch(to_branch_name=None, remote_name=None):
    repo = git.Repo(os.getcwd())
    g = repo.git
    source_branch_name = repo.head.reference

    g.checkout(to_branch_name)
    if remote_name:
        g.pull(remote_name, to_branch_name)

    # GitPython does not support merge --no-ff or what?
    git_cmd = git.cmd.Git(os.getcwd())
    no_ff_commit = 'Merge branch "{}"'.format(source_branch_name)
    git_cmd.execute(('git', 'merge', '--no-ff', '-m', no_ff_commit, str(source_branch_name)))

    if remote_name:
        g.push(remote_name, to_branch_name)

    g.checkout(source_branch_name)
