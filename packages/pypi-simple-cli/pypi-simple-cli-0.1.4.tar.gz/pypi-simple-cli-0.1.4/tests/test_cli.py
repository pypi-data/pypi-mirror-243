import os
import pathlib

import pytest
import requests_mock
from click.testing import CliRunner

from pypi_simple_cli import __main__

PYPI_SIMPLE_ENDPOINT: str = "https://pypi.org/simple/"
DATA_DIR = pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / "data"


@requests_mock.Mocker(kw="mock")
def test_list_indexd(**kwargs):
    with (DATA_DIR / "fake_page.html").open() as f:
        kwargs["mock"].get(f"{PYPI_SIMPLE_ENDPOINT}indexd/", text=f.read())
    runner = CliRunner()
    result = runner.invoke(
        __main__.main,
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
        __main__.main,
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
    result = runner.invoke(
        __main__.main,
        [
            "-p",
            pattern,
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
        __main__.main,
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
        __main__.main,
        args=[
            f"--release-stage={stage}",
            "latest",
            "indexd",
        ],
    )
    assert result.output == expected

    result = runner.invoke(
        __main__.main,
        args=[
            "-s",
            stage,
            "latest",
            "indexd",
        ],
    )
    assert result.output == expected


def test_endpoint_from_env(monkeypatch):
    url = "http://fake.com"
    with monkeypatch.context() as m:
        m.setenv("PIP_INDEX_URL", url)
        runner = CliRunner()
        result = runner.invoke(
            __main__.main,
            args=[
                "latest",
                "indexd",
            ],
        )
        assert result.exception.url == f"{url}/indexd/"


def test_endpoint_from_arg():
    url = "http://fake.com"
    runner = CliRunner()
    result = runner.invoke(
        __main__.main,
        args=[
            f"--endpoint={url}",
            "latest",
            "indexd",
        ],
    )
    assert result.exception.url == f"{url}/indexd/"

    result = runner.invoke(
        __main__.main,
        args=[
            "-e",
            url,
            "latest",
            "indexd",
        ],
    )
    assert result.exception.url == f"{url}/indexd/"
