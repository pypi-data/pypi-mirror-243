# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from fedora_messaging import message

SCHEMA_URL = "http://fedoraproject.org/message-schema/"


class FedoraMessagingGitHookMessage(message.Message):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by Fedora Messaging Git Hook.
    """

    @property
    def app_name(self):
        return "Git"

    @property
    def app_icon(self):
        return "https://apps.fedoraproject.org/img/icons/git-logo.png"

    # @property
    # def url(self):
    #     return None

    @property
    def agent_name(self):
        """The username of the user who initiated the action that generated this message."""
        return self.body.get("agent")

    @property
    def usernames(self):
        """List of users affected by the action that generated this message."""
        return [self.agent_name]

    @property
    def groups(self):
        """List of groups affected by the action that generated this message."""
        group = self.body.get("group")
        return [group] if group else []

    def _repo_if_namespace(self, namespace):
        """List of packages affected by the action that generated this message."""
        if self.body["commit"].get("namespace") == namespace:
            return [self.body["commit"]["repo"]]
        return []

    @property
    def packages(self):
        """List of packages affected by the action that generated this message."""
        return self._repo_if_namespace("rpms")

    @property
    def containers(self):
        """List of containers affected by the action that generated this message."""
        return self._repo_if_namespace("container")

    @property
    def modules(self):
        """List of modules affected by the action that generated this message."""
        return self._repo_if_namespace("modules")

    @property
    def flatpaks(self):
        """List of flatpaks affected by the action that generated this message."""
        return self._repo_if_namespace("flatpaks")
