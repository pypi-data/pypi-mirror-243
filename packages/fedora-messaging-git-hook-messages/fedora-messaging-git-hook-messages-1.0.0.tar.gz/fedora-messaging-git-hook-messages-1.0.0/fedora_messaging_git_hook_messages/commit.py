# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from .base import SCHEMA_URL, FedoraMessagingGitHookMessage

COMMIT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "username": {"type": "string"},
        "summary": {"type": "string"},
        "message": {"type": "string"},
        "stats": {
            "type": "object",
            "properties": {
                "files": {"type": "object"},
                "total": {
                    "type": "object",
                    "properties": {
                        "additions": {"type": "number"},
                        "deletions": {"type": "number"},
                        "lines": {"type": "number"},
                        "files": {"type": "number"},
                    },
                },
            },
        },
        "rev": {"type": "string"},
        "path": {"type": "string"},
        "repo": {"type": "string"},
        "namespace": {"type": ["string", "null"]},
        "branch": {"type": "string"},
        "patch": {"type": "string"},
        "date": {"type": "string"},
        "url": {"type": ["string", "null"]},
    },
    "required": [
        "name",
        "email",
        "username",
        "summary",
        "message",
        "stats",
        "rev",
        "path",
        "repo",
        "namespace",
        "branch",
        "patch",
        "date",
        "url",
    ],
}

STR_TEMPLATE = """From {hash} Mon Sep 17 00:00:00 2001
From: {author_name} <{author_email}>
Date: {date}
Subject: {summary}

{content}
---

{patch}
"""


class CommitV1(FedoraMessagingGitHookMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by Fedora Messaging Git Hook when a new commit is received.
    """

    topic = "git.receive"

    body_schema = {
        "id": SCHEMA_URL + topic,
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for messages sent when a new thing is created",
        "type": "object",
        "properties": {"agent": {"type": "string"}, "commit": COMMIT_SCHEMA},
        "required": ["agent", "commit"],
    }

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        commit = self.body["commit"]
        return STR_TEMPLATE.format(
            hash=commit["rev"],
            author_name=commit["name"],
            author_email=commit["email"],
            date=commit["date"],
            summary=commit["summary"],
            content=commit["message"],
            patch=commit["patch"],
        )

    @property
    def summary(self):
        """Return a summary of the message."""
        repo_name = self.body["commit"]["repo"]
        namespace = self.body["commit"].get("namespace")
        if namespace:
            repo_name = f"{namespace}/{repo_name}"
        return '{agent} pushed to {repo} ({branch}). "{summary}"'.format(
            agent=self.agent_name,
            repo=repo_name,
            branch=self.body["commit"]["branch"],
            summary=self.body["commit"]["summary"],
        )

    @property
    def url(self):
        return self.body["commit"]["url"]
