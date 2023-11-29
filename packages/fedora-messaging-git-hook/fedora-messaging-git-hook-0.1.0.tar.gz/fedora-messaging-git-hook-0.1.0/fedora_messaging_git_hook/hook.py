# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

import getpass
import os
import subprocess as sp
import sys
import traceback
from collections import defaultdict

import backoff
import click
import fedora_messaging.api
import fedora_messaging.config
import fedora_messaging.exceptions
import pygit2


def revs_between(repo, head, base):
    """Yield revisions between HEAD and BASE."""
    try:
        base = repo.revparse_single(base)
    except KeyError:
        crange = str(head.id)
    else:
        crange = f"{head.id}...{base.id}"

    # pygit2 can't do a rev-list yet, so we have to shell out.. silly.
    proc = sp.run(
        ["/usr/bin/git", "rev-list", crange],  # noqa: S603
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        cwd=repo.workdir or repo.path,
        universal_newlines=True,
    )
    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr)
        raise OSError(f"git rev-list failed: {proc.stdout!r}, err: {proc.stderr!r}")

    return [line.strip() for line in proc.stdout.strip().split("\n")]


def build_stats(repo, commit):
    files = defaultdict(lambda: defaultdict(int))

    # Calculate diffs against all parent commits
    diffs = [repo.diff(parent, commit) for parent in commit.parents]
    # Unless this is the first commit, with no parents.
    diffs = diffs or [commit.tree.diff_to_tree(swap=True)]

    for diff in diffs:
        for patch in diff:
            if hasattr(patch, "new_file_path"):
                path = patch.new_file_path
            else:
                path = patch.delta.new_file.path

            if hasattr(patch, "additions"):
                files[path]["additions"] += patch.additions
                files[path]["deletions"] += patch.deletions
                files[path]["lines"] += patch.additions + patch.deletions
            else:
                files[path]["additions"] += patch.line_stats[1]
                files[path]["deletions"] += patch.line_stats[2]
                files[path]["lines"] += patch.line_stats[1] + patch.line_stats[2]

    total = defaultdict(int)
    for filename, stats in files.items():
        files[filename] = dict(stats)
        total["additions"] += stats["additions"]
        total["deletions"] += stats["deletions"]
        total["lines"] += stats["lines"]
        total["files"] += 1

    return dict(files), dict(total)


def build_commit(repo, with_namespace, rev, branch):
    commit = repo.revparse_single(str(rev))

    # Tags are a little funny, and vary between versions of pygit2, so we'll
    # just ignore them as far as fedmsg is concerned.
    # abompard: I'm not finding a way to have git rev-list output the tags, so
    # I think we don't need the following test. But as adamwill would say,
    # "don't remove the fence if you don't know why it's there".
    if isinstance(commit, pygit2.Tag):
        return None

    files, total = build_stats(repo, commit)
    username = getpass.getuser()
    repo_path = os.path.abspath(repo.workdir or repo.path)
    if repo_path.endswith(".git"):
        repo_path = repo_path[:-4]
    if with_namespace:
        namespace = repo_path.split(os.path.sep)[-2]
    else:
        namespace = None
    repo_name = os.path.basename(repo_path)

    return dict(
        name=commit.author.name,
        email=commit.author.email,
        username=username,
        summary=commit.message.split("\n")[0],
        message=commit.message,
        stats=dict(
            files=files,
            total=total,
        ),
        rev=str(rev),
        path=repo.workdir or repo.path,
        repo=repo_name,
        namespace=namespace,
        branch=branch,
    )


def process(repo, with_namespace, lines):
    seen = []
    for line in lines:
        base, head, branch = line.split(" ")
        branch = "/".join(branch.split("/")[2:]).strip()

        try:
            head = repo.revparse_single(head)
        except KeyError:
            # This means they are deleting this branch.. and we don't have a fedmsg
            # for that (yet?).  It is disallowed by dist-git in Fedora anyways.
            continue

        revs = revs_between(repo, head, base)
        commits = [build_commit(repo, with_namespace, rev, branch) for rev in revs]

        click.echo(f"* Publishing information for {len(commits)} commits")
        for commit in reversed(commits):
            if commit is None:
                continue

            # Keep track of whether or not we have already published this commit on
            # another branch or not.  It is conceivable that someone could make a
            # commit to a number of branches, and push them all at the same time.
            # Make a note in the fedmsg payload so we can try to reduce spam at a
            # later stage.
            if commit["rev"] in seen:
                commit["seen"] = True
            else:
                commit["seen"] = False
                seen.append(commit["rev"])

            publish(commit)


def backoff_hdlr(details):
    click.echo(
        f"Publishing message failed. Retrying. {traceback.format_tb(sys.exc_info()[2])}", err=True
    )


def giveup_hdlr(details):
    click.echo(
        f"Publishing message failed. Giving up. {traceback.format_tb(sys.exc_info()[2])}", err=True
    )


@backoff.on_exception(
    backoff.expo,
    (fedora_messaging.exceptions.ConnectionException, fedora_messaging.exceptions.PublishException),
    max_tries=3,
    on_backoff=backoff_hdlr,
    on_giveup=giveup_hdlr,
)
def publish(commit):
    message = fedora_messaging.api.Message(
        topic="git.receive", body=dict(commit=commit, agent=commit["username"])
    )
    fedora_messaging.api.publish(message)
