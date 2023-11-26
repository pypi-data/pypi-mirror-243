from __future__ import annotations

from pathlib import Path
from smtplib import SMTPServerDisconnected

from pytest import raises

from utilities.email import InvalidContentsError, send_email
from utilities.pytest import is_pytest


class TestSendEmail:
    def test_main(self) -> None:
        with raises(SMTPServerDisconnected):
            send_email("no-reply@test.com", ["user@test.com"], disable=None)

    def test_subject(self) -> None:
        with raises(SMTPServerDisconnected):
            send_email(
                "no-reply@test.com", ["user@test.com"], subject="Subject", disable=None
            )

    def test_contents_str(self) -> None:
        with raises(SMTPServerDisconnected):
            send_email(
                "no-reply@test.com",
                ["user@test.com"],
                subject="Subject",
                contents="contents",
                disable=None,
            )

    def test_attachment(self, tmp_path: Path) -> None:
        file = tmp_path.joinpath("file")
        file.touch()
        with raises(SMTPServerDisconnected):
            send_email(
                "no-reply@test.com",
                ["user@test.com"],
                subject="Subject",
                attachments=[file],
                disable=None,
            )

    def test_invalid_contents(self) -> None:
        with raises(InvalidContentsError):
            send_email(
                "no-reply@test.com",
                ["user@test.com"],
                subject="Subject",
                contents=object(),
                disable=None,
            )

    def test_disable(self) -> None:
        send_email("no-reply@test.com", ["user@test.com"], disable=is_pytest)
