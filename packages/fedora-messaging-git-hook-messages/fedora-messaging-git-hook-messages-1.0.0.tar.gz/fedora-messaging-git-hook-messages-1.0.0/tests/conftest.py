# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import pytest


@pytest.fixture
def dummy_empty_commit():
    return {
        "name": "Dummy User",
        "email": "dummy@example.com",
        "username": "dummyuser",
        "summary": "initial commit",
        "message": "initial commit\n",
        "stats": {"files": {}, "total": {}},
        "rev": "e03df21592dcdc201cebbc578ea0644645b825a6",
        "path": "/tmp/pytest-of-dummyuser/pytest-109/test_namespace0/dummyns/dummyrepo/",
        "repo": "dummyrepo",
        "namespace": "dummyns",
        "branch": "main",
        "patch": "",
        "date": "2023-11-30T10:42:31+01:00",
        "url": None,
    }


@pytest.fixture
def dummy_commit():
    return {
        "name": "Dummy User",
        "email": "dummy@example.com",
        "username": "dummyuser",
        "summary": "second commit",
        "message": "second commit\n",
        "stats": {
            "files": {"something.txt": {"additions": 0, "deletions": 0, "lines": 0}},
            "total": {"additions": 0, "deletions": 0, "lines": 0, "files": 1},
        },
        "rev": "3aa6642b0990d1f6a0e0ce7373c8ad37d2f980ce",
        "path": "/tmp/pytest-of-dummyuser/pytest-109/test_namespace0/dummyns/dummyrepo/",
        "repo": "dummyrepo",
        "namespace": "dummyns",
        "branch": "main",
        "patch": (
            "diff --git a/something.txt b/something.txt\nnew file mode 100644\n"
            "index 0000000..e69de29\n--- /dev/null\n+++ b/something.txt\n"
        ),
        "date": "2023-11-30T10:42:31+01:00",
        "url": "http://example.com/repo/c/3aa6642b0990d1f6a0e0ce7373c8ad37d2f980ce?branch=main",
    }
