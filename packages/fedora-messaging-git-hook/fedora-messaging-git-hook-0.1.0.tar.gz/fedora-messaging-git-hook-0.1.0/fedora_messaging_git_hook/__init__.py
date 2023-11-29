# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later


try:
    import importlib.metadata

    __version__ = importlib.metadata.version("fedora_messaging_git_hook")
except ImportError:
    import importlib_metadata

    __version__ = importlib_metadata.version("fedora_messaging_git_hook")
