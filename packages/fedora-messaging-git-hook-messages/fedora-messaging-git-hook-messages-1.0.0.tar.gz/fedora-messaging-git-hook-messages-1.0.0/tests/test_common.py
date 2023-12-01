# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Unit tests for common properties of the message schemas."""

from fedora_messaging_git_hook_messages.commit import CommitV1


def test_properties(dummy_commit):
    """Assert some properties are correct."""
    body = {
        "agent": "dummy-user",
        "commit": dummy_commit,
    }
    message = CommitV1(body=body)

    assert message.app_name == "Git"
    assert message.app_icon == "https://apps.fedoraproject.org/img/icons/git-logo.png"
    assert message.agent_name == "dummy-user"
    assert message.agent_avatar == (
        "https://seccdn.libravatar.org/avatar/"
        "18e8268125372e35f95ef082fd124e9274d46916efe2277417fa5fecfee31af1"
        "?s=64&d=retro"
    )
    assert message.usernames == ["dummy-user"]
