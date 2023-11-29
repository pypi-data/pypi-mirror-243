import os
import pathlib

import pytest
import requests_mock
from click.testing import CliRunner

from pypi_simple_cli import cli

PYPI_SIMPLE_ENDPOINT: str = "https://pypi.org/simple/"
DATA_DIR = pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / "data"


@requests_mock.Mocker(kw="mock")
def test_list_indexd(**kwargs):
    with (DATA_DIR / "fake_page.html").open() as f:
        kwargs["mock"].get(f"{PYPI_SIMPLE_ENDPOINT}indexd/", text=f.read())
    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        [
            "list",
            "indexd",
        ],
    )
    assert result.output == (
        "1.0.0.dev6+feat.dev.2298.use.different.post.fix\n"
        "1.0.0\n1.2.3rc4\n1.2.3rc5\n1.2.4b4\n1.2.5a4\n2.13.3.dev2\n"
        "3.0.2.dev6+feat.dev.2298.use.different.post.fix.for.version\n"
    )


@requests_mock.Mocker(kw="mock")
@pytest.mark.parametrize(
    "pattern", ["different.post", "different\.post", "different.*fix"]
)
def test_list_indexd_with_regex(pattern, **kwargs):
    with (DATA_DIR / "fake_page.html").open() as f:
        kwargs["mock"].get(f"{PYPI_SIMPLE_ENDPOINT}indexd/", text=f.read())
    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        [
            f"--pattern={pattern}",
            "list",
            "indexd",
        ],
    )
    assert result.output == (
        "1.0.0.dev6+feat.dev.2298.use.different.post.fix\n"
        "3.0.2.dev6+feat.dev.2298.use.different.post.fix.for.version\n"
    )


@requests_mock.Mocker(kw="mock")
def test_latest_indexd(**kwargs):
    with (DATA_DIR / "fake_page.html").open() as f:
        kwargs["mock"].get(f"{PYPI_SIMPLE_ENDPOINT}indexd/", text=f.read())
    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        [
            "latest",
            "indexd",
        ],
    )
    assert (
        result.output == "3.0.2.dev6+feat.dev.2298.use.different.post.fix.for.version"
    )


@requests_mock.Mocker(kw="mock")
@pytest.mark.parametrize(
    "stage,expected",
    [
        ("all", "3.0.2.dev6+feat.dev.2298.use.different.post.fix.for.version"),
        ("dev", "3.0.2.dev6+feat.dev.2298.use.different.post.fix.for.version"),
        ("alpha", "1.2.5a4"),
        ("beta", "1.2.4b4"),
        ("rc", "1.2.3rc5"),
        ("final", "1.0.0"),
    ],
)
def test_latest_indexd_with_stage(stage, expected, **kwargs):
    with (DATA_DIR / "fake_page.html").open() as f:
        kwargs["mock"].get(f"{PYPI_SIMPLE_ENDPOINT}indexd/", text=f.read())
    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        [
            f"--release-stage={stage}",
            "latest",
            "indexd",
        ],
    )
    assert result.output == expected
