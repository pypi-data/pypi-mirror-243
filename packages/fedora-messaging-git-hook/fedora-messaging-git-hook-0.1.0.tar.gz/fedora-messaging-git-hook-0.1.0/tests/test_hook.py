# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from subprocess import run, PIPE
from contextlib import contextmanager
from unittest import mock

import pytest
from click.testing import CliRunner
from fedora_messaging import api as fm_api
from fedora_messaging.testing import mock_sends


from fedora_messaging_git_hook import cli


@contextmanager
def pushd(path):
    old = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old)


@pytest.fixture(autouse=True)
def mock_username(monkeypatch):
    monkeypatch.setattr(
        "fedora_messaging_git_hook.hook.getpass.getuser", mock.Mock(return_value="dummyuser")
    )


def _make_git_repo(path, bare=False):
    os.makedirs(path)
    cmd = ["git", "init", path.as_posix()]
    if bare:
        cmd.insert(2, "--bare")
        hookpath = path
    else:
        hookpath = path / ".git"
    hookpath = hookpath / "hooks" / "post-receive"
    run(cmd, check=True)
    with open(hookpath, "w") as fh:
        fh.write("#!/bin/sh\nwhile read oval nval ref; do echo $oval $nval $ref; done\n")
    run(["chmod", "+x", hookpath.as_posix()])


def _get_last_commit_id(git_dir, branch="main"):
    return run(
        ["git", "rev-list", "-1", branch],
        stdout=PIPE,
        cwd=git_dir,
        check=True,
        universal_newlines=True,
    ).stdout.strip()


def run_hook(git_dir, args=None, stdin=None):
    env = os.environ.copy()
    env["GIT_DIR"] = git_dir.as_posix()
    if stdin is None:
        last_commit_id = _get_last_commit_id(git_dir)
        stdin = f"0000000000000000000000000000000000000000 {last_commit_id} refs/heads/main\n"
    runner = CliRunner()
    result = runner.invoke(cli.main, args or [], input="".join(stdin), env=env)
    return result


def _make_a_couple_commits(repo_path):
    with pushd(repo_path):
        run(["git", "config", "user.name", "Dummy User"])
        run(["git", "config", "user.email", "dummy@example.com"])
        run(["git", "commit", "--allow-empty", "-m", "initial commit"])
        open("something.txt", "w").close()
        run(["git", "add", "."])
        run(["git", "commit", "-a", "-m", "second commit"])


def test_basic(tmp_path):
    git_repo = tmp_path / "repo"
    _make_git_repo(git_repo)
    _make_a_couple_commits(git_repo)
    with mock_sends(fm_api.Message, fm_api.Message):
        result = run_hook(git_repo / ".git")
        # print(result.stdout, result.exc_info)
        sent_messages = [call[0][0] for call in fm_api._twisted_publish.call_args_list]
    assert len(sent_messages) == 2
    assert result.exit_code == 0
    assert all(m.body["agent"] == "dummyuser" for m in sent_messages)
    assert all(m.body["commit"]["branch"] == "main" for m in sent_messages)
    assert all(m.body["commit"]["username"] == "dummyuser" for m in sent_messages)
    assert all(m.body["commit"]["name"] == "Dummy User" for m in sent_messages)
    assert all(m.body["commit"]["email"] == "dummy@example.com" for m in sent_messages)
    assert all(m.body["commit"]["namespace"] is None for m in sent_messages)
    assert all(m.body["commit"]["repo"] == "repo" for m in sent_messages)
    assert all(m.body["commit"]["path"] == (git_repo.as_posix() + "/") for m in sent_messages)
    assert [m.body["commit"]["summary"] for m in sent_messages] == [
        "initial commit",
        "second commit",
    ]
    assert sent_messages[1].body["commit"]["stats"] == {
        "files": {"something.txt": {"additions": 0, "deletions": 0, "lines": 0}},
        "total": {"additions": 0, "deletions": 0, "files": 1, "lines": 0},
    }


def test_bare(tmp_path):
    git_repo = tmp_path / "repo.git"
    _make_git_repo(git_repo, bare=True)
    git_clone = tmp_path.joinpath("repo_clone")
    run(["git", "clone", git_repo.as_posix(), git_clone.as_posix()])
    _make_a_couple_commits(git_clone)
    run(["git", "push"], cwd=git_clone, check=True)
    with mock_sends(fm_api.Message, fm_api.Message):
        result = run_hook(git_repo)
        # print(result.stdout, result.exc_info)
        sent_messages = [call[0][0] for call in fm_api._twisted_publish.call_args_list]
    assert result.exit_code == 0
    assert len(sent_messages) == 2
    assert all(m.body["commit"]["repo"] == "repo" for m in sent_messages)
    assert all(m.body["commit"]["path"] == (git_repo.as_posix() + "/") for m in sent_messages)


def test_namespace(tmp_path):
    with open(tmp_path / "config.toml", "w") as fmconfig:
        fmconfig.write(
            """
# amqp_url = "amqp://username:password@rabbitmq.example.com/vhost"
[consumer_config]
excluded_paths = []
with_namespace = true
"""
        )
    git_repo = tmp_path / "dummyns" / "dummyrepo"
    _make_git_repo(git_repo)
    _make_a_couple_commits(git_repo)
    with mock_sends(fm_api.Message, fm_api.Message):
        result = run_hook(
            git_repo / ".git", ["--config", tmp_path.joinpath("config.toml").as_posix()]
        )
        # print(result.stdout, result.exc_info)
        sent_messages = [call[0][0] for call in fm_api._twisted_publish.call_args_list]
    assert result.exit_code == 0
    assert len(sent_messages) == 2
    assert all(m.body["commit"]["repo"] == "dummyrepo" for m in sent_messages)
    assert all(m.body["commit"]["namespace"] == "dummyns" for m in sent_messages)


def test_delete_branch(tmp_path):
    git_repo = tmp_path / "repo"
    _make_git_repo(git_repo)
    _make_a_couple_commits(git_repo)
    with mock_sends():
        last_commit_id = _get_last_commit_id(git_repo)
        hook_input = f"{last_commit_id} 0000000000000000000000000000000000000000 refs/heads/main\n"
        result = run_hook(git_repo, stdin=hook_input)
        # print(result.stdout, result.exc_info)
    assert result.exit_code == 0
