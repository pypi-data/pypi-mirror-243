import enum
import re

import click
from packaging.version import Version, parse
from pypi_simple import PyPISimple


class ReleaseStage(enum.IntEnum):
    all = 0
    dev = 1
    alpha = 2
    beta = 3
    rc = 4
    final = 5


@click.group()
@click.option("--endpoint", help="The base URL of the simple API instance to query")
@click.option(
    "--release-stage",
    type=click.Choice(
        list(i.name for i in ReleaseStage),
        case_sensitive=False,
    ),
    default="all",
    help="Lowest release stage",
)
@click.option("--pattern", help="Use python regex to match the version.")
@click.pass_context
def main(ctx, endpoint, release_stage, pattern):
    ctx.ensure_object(dict)
    if endpoint is None:
        simple = PyPISimple()
    else:
        simple = PyPISimple(endpoint=endpoint)

    ctx.obj["simple"] = simple
    ctx.obj["release_stage"] = release_stage
    ctx.obj["pattern"] = pattern


def filter_versions(ctx, package, version_prefix):
    with ctx.obj["simple"] as client:
        page = client.get_project_page(package)

    if page.versions:
        versions = page.versions
    else:
        versions = sorted(
            set(
                pkg.version or pkg.filename
                for pkg in page.packages
                if pkg.filename != "Parent Directory"
            ),
            key=parse,
        )
    if version_prefix:
        versions = (v for v in versions if v.startswith(version_prefix))
    release_stage = ReleaseStage[ctx.obj["release_stage"].lower()]
    if release_stage > ReleaseStage.dev:
        versions = (v for v in versions if Version(v).is_devrelease is False)
    if release_stage.value > ReleaseStage.alpha:
        versions = (
            v for v in versions if Version(v).pre is None or Version(v).pre[0] != "a"
        )
    if release_stage.value > ReleaseStage.beta:
        versions = (
            v for v in versions if Version(v).pre is None or Version(v).pre[0] != "b"
        )
    if release_stage.value > ReleaseStage.rc:
        versions = (v for v in versions if Version(v).is_prerelease is False)

    pattern = ctx.obj["pattern"]
    if pattern:
        versions = (v for v in versions if re.search(pattern, v))
    return versions


@click.command("list")
@click.argument("package")
@click.argument("version_prefix", required=False)
@click.pass_context
def list_versions(ctx, package, version_prefix):
    versions = filter_versions(ctx, package, version_prefix)

    for version in versions:
        print(version)


@click.command("latest")
@click.argument("package")
@click.argument("version_prefix", required=False)
@click.pass_context
def latest_version(ctx, package, version_prefix):
    versions = filter_versions(ctx, package, version_prefix)
    print(list(versions)[-1], end="")


main.add_command(list_versions)
main.add_command(latest_version)


if __name__ == "__main__":
    main(obj={})
