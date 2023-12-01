#!/usr/bin/env python
"""Tests for `environment_backups` package."""

from click.testing import CliRunner

from environment_backups import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    result_lines = result.output.split('\n')
    expected_lines = [
        "Usage: main [OPTIONS] COMMAND [ARGS]...",
        "",
        "  Main entrypoint.",
        "",
        "Options:",
        "  --help  Show this message and exit.",
        "",
        "Commands:",
        "  about",
        "  backup",
        "  config  Configuration entrypoint.",
        ""
    ]
    assert len(result_lines) == len(expected_lines)
    assert result.exit_code == 0
    for i, line in enumerate(result_lines):
        assert line == expected_lines[i]


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli.main, ['--help'])

    assert result.exit_code == 0
    result_lines = result.output.split('\n')

    expected_lines = [
        "Usage: main [OPTIONS] COMMAND [ARGS]...",
        "",
        "  Main entrypoint.",
        "",
        "Options:",
        "  --help  Show this message and exit.",
        "",
        "Commands:",
        "  about",
        "  backup",
        "  config  Configuration entrypoint.",
        ""
    ]
    assert len(result_lines) == len(expected_lines)
    assert result.exit_code == 0
    for i, line in enumerate(result_lines):
        assert line == expected_lines[i]
