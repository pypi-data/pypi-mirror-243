# Fedora Messaging Git Hook

This repo contains a git post-receive hook to send messages on the Fedora Messaging bus.

The full documentation is [on ReadTheDocs](https://fedora-messaging-git-hook.readthedocs.io).

You can install it [from PyPI](https://pypi.org/project/fedora-messaging-git-hook/).

![PyPI](https://img.shields.io/pypi/v/fedora-messaging-git-hook.svg)
![Supported Python versions](https://img.shields.io/pypi/pyversions/fedora-messaging-git-hook.svg)
![Build status](http://github.com/fedora-infra/fedora-messaging-git-hook/actions/workflows/main.yml/badge.svg?branch=develop)
![Documentation](https://readthedocs.org/projects/fedora-messaging-git-hook/badge/?version=latest)


The development layout is a bit outdated (no poetry, setup.cfg, MANIFEST.in,
etc.) because we need to work with Python 3.6, and the Python ecosystem ship
has sailed a long time ago for that version.
