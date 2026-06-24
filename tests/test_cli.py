"""Minimal tests for the CLI entrypoint."""

from click.testing import CliRunner
import pytest

import ne_loader.cli as cli
from ne_loader.map_loader import Resolution


def test_cli_delegates_to_get_natural_earth(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure the CLI forwards arguments to map_loader.get_natural_earth."""
    called = {}

    def fake_get(category: str, name: str, res: Resolution):
        called["args"] = (category, name, res)

    monkeypatch.setattr(cli.map_loader, "get_natural_earth", fake_get)

    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        ["download-get", "Cultural", "admin_0_countries", "--res", "50m"],
    )

    assert result.exit_code == 0
    assert called["args"] == ("Cultural", "admin_0_countries", "50m")
