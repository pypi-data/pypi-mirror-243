# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Unit tests for the message schema."""


import pytest
from jsonschema import ValidationError

from fedora_messaging_git_hook_messages.commit import CommitV1


def test_minimal(dummy_empty_commit):
    """
    Assert the message schema validates a message with the required fields.
    """
    body = {
        "agent": "dummy-user",
        "commit": dummy_empty_commit,
    }
    message = CommitV1(body=body)
    message.validate()
    assert message.url is None


def test_full(dummy_commit):
    """
    Assert the message schema validates a message with the required fields.
    """
    body = {
        "agent": "dummy-user",
        "commit": dummy_commit,
    }
    message = CommitV1(body=body)
    message.validate()
    assert (
        message.url
        == "http://example.com/repo/c/3aa6642b0990d1f6a0e0ce7373c8ad37d2f980ce?branch=main"
    )


def test_missing_fields():
    """Assert an exception is actually raised on validation failure."""
    minimal_message = {
        "agent": "dummy-user",
        "commit": {"repo": "dummy"},
    }
    message = CommitV1(body=minimal_message)
    with pytest.raises(ValidationError):
        message.validate()


def test_str(dummy_commit):
    """Assert __str__ produces a human-readable message."""
    body = {
        "agent": "dummy-user",
        "commit": dummy_commit,
    }
    expected_str = """From 3aa6642b0990d1f6a0e0ce7373c8ad37d2f980ce Mon Sep 17 00:00:00 2001
From: Dummy User <dummy@example.com>
Date: 2023-11-30T10:42:31+01:00
Subject: second commit

second commit

---

diff --git a/something.txt b/something.txt
new file mode 100644
index 0000000..e69de29
--- /dev/null
+++ b/something.txt

"""
    message = CommitV1(body=body)
    message.validate()
    assert expected_str == str(message)


def test_summary(dummy_commit):
    """Assert the summary is correct."""
    body = {
        "agent": "dummy-user",
        "commit": dummy_commit,
    }
    expected_summary = 'dummy-user pushed to dummyns/dummyrepo (main). "second commit"'
    message = CommitV1(body=body)
    assert expected_summary == message.summary


def test_summary_no_namespace(dummy_commit):
    """Assert the summary is correct."""
    dummy_commit["namespace"] = None
    body = {
        "agent": "dummy-user",
        "commit": dummy_commit,
    }
    expected_summary = 'dummy-user pushed to dummyrepo (main). "second commit"'
    message = CommitV1(body=body)
    assert expected_summary == message.summary


NAMESPACE_TO_ATTRIBUTE = {
    "rpms": "packages",
    "container": "containers",
    "modules": "modules",
    "flatpaks": "flatpaks",
}


@pytest.mark.parametrize("namespace", ["rpms", "container", "modules", "flatpaks"])
def test_artifact(dummy_commit, namespace):
    dummy_commit["namespace"] = namespace
    body = {
        "agent": "dummy-user",
        "commit": dummy_commit,
    }
    message = CommitV1(body=body)
    for artifact_ns, artifact_type in NAMESPACE_TO_ATTRIBUTE.items():
        artifact_list = getattr(message, artifact_type)
        if artifact_ns == namespace:
            assert artifact_list == ["dummyrepo"]
        else:
            assert artifact_list == []
