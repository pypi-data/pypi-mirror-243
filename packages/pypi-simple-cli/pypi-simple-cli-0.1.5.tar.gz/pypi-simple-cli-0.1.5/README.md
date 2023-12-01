# pypi-simple-cli
A wrapper for [pypi-simple](https://github.com/jwodder/pypi-simple/tree/master)


|         |                                                                                                                                                                                                                                                                                                                                                                                                     |
|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD   | [![CI - Test](https://github.com/asurinsaka/pypi-simple-cli/actions/workflows/pytest.yaml/badge.svg)](https://github.com/asurinsaka/pypi-simple-cli/actions/workflows/pytest.yaml)  [![CI - Release](https://github.com/asurinsaka/pypi-simple-cli/actions/workflows/publish-to-test-pypi.yml/badge.svg)](https://github.com/asurinsaka/pypi-simple-cli/actions/workflows/publish-to-test-pypi.yml) |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/pypi-simple-cli?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/pypi-simple-cli/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pypi-simple-cli.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/pypi-simple-cli/)                                                                         |
| Meta    | [![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![License - Apache](https://img.shields.io/github/license/asurinsaka/pypi-simple-cli)](https://spdx.org/licenses/)                                                                                                                                                               |


## Example Usage:

```shell
> pypi-simple-cli list pypi-simple-cli
0.1.1

> pypi-simple-cli latest pypi-simple-cli
0.1.1

> pypi-simple-cli list requests 2.9
2.9.0
2.9.1
2.9.2

> pypi-simple-cli --endpoint=https://nexus.osdc.io/service/rest/repository/browse/pypi-all/ --release-stage=final list gdcdatamodel2
2.6.8
3.0.0

> pypi-simple-cli --endpoint=https://nexus.osdc.io/service/rest/repository/browse/pypi-all/ --pattern='use.*fix' list gdcdatamodel2
3.0.2.dev6+feat.dev.2298.use.different.post.fix.for.version
3.0.2.dev7+feat.dev.2298.use.different.post.fix.for.version

> pip install requests==$(pypi-simple-cli latest requests 2.30)
Collecting requests==2.30.0
  Downloading requests-2.30.0-py3-none-any.whl (62 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 62.5/62.5 kB 2.5 MB/s eta 0:00:00
Requirement already satisfied: charset-normalizer<4,>=2 in ./venv37/lib/python3.7/site-packages (from requests==2.30.0) (3.3.2)
Requirement already satisfied: idna<4,>=2.5 in ./venv37/lib/python3.7/site-packages (from requests==2.30.0) (3.6)
Requirement already satisfied: urllib3<3,>=1.21.1 in ./venv37/lib/python3.7/site-packages (from requests==2.30.0) (2.0.7)
Requirement already satisfied: certifi>=2017.4.17 in ./venv37/lib/python3.7/site-packages (from requests==2.30.0) (2023.11.17)
Installing collected packages: requests
  Attempting uninstall: requests
    Found existing installation: requests 2.31.0
    Uninstalling requests-2.31.0:
      Successfully uninstalled requests-2.31.0
Successfully installed requests-2.30.0

```
