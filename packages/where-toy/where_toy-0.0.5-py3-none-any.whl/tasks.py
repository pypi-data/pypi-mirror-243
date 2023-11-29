""" tasks file (see invoke.py) """

import os
import sys
import toml
import shutil
import logging
import jmespath

from invoke import task
from pathlib import Path

logger = logging.getLogger()

root_folder = Path(__file__).parent


def get_config(folder):
    """ Parse pyproject.toml file """

    pyproject = folder.joinpath("pyproject.toml").resolve()

    if not pyproject.exists():
        raise FileNotFoundError(str(pyproject))

    return toml.load(pyproject)


@task
def clean(ctx):
    patterns = ['build', 'dist']
    for pattern in patterns:
        ctx.run("rm -rf {}".format(pattern))


@task
def build(ctx):
    ctx.run("python -mbuild --wheel")


@task
def publish(ctx, test_only=False):
    """ Build project(s) from current folder or sub-folders """

    if test_only:
        ctx.run("twine upload --repository testpypi dist/*")
    else:
        ctx.run("twine upload dist/*")
