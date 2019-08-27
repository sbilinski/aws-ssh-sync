# -*- coding: utf-8 -*-

import aws_ssh_sync
import pytest
import re


def test_help_to_stdout(capsys):

    with pytest.raises(SystemExit) as wrapped_exception:
        aws_ssh_sync.main("-h")

    assert wrapped_exception.type == SystemExit
    assert wrapped_exception.value.code == 0

    out, err = capsys.readouterr()

    assert err == ""
    assert "--help" in out


def test_version_to_stdout(capsys):

    version_pattern = re.compile("^[0-9]+.[0-9]+.[0-9]+$")

    with pytest.raises(SystemExit) as wrapped_exception:
        aws_ssh_sync.main("-v")

    assert wrapped_exception.type == SystemExit
    assert wrapped_exception.value.code == 0

    out, err = capsys.readouterr()

    assert err == ""
    assert version_pattern.match(out)
