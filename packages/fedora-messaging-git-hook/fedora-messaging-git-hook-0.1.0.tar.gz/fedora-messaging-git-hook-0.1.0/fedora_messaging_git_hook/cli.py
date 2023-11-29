# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys

import click
import pygit2
from fedora_messaging.config import conf

from .hook import process


@click.command()
@click.option("--config", help="Fedora Messaging configuration file")
def main(config):
    conf.load_config(config)

    # Use $GIT_DIR to determine where this repo is.
    abspath = os.path.abspath(os.environ["GIT_DIR"])

    excluded_paths = conf["consumer_config"].get("excluded_paths", [])
    if any([path in abspath for path in excluded_paths]):
        return

    with_namespace = conf["consumer_config"].get("with_namespace", False)

    repo = pygit2.Repository(abspath)
    # Read in all the rev information git-receive-pack hands us.
    click.echo("Emitting a message to the fedora-messaging message bus.")
    process(repo, with_namespace, list(sys.stdin.readlines()))
