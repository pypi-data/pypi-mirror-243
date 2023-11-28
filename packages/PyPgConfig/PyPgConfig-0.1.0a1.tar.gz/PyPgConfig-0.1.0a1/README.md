<p align="center">

  <h1 align="center">PyPgConfig🐘❤️🐍</h1>
  <p align="center">
  <strong>Access pg_config from Python</strong>
    <br> <br />
    <a href="#installation"><strong> Installation </strong></a> |
    <a href="#usage"><strong> Usage </strong></a> |

   </p>
<p align="center">

<p align="center">
<a href="https://pypi.org/project/PyPgConfig/"><img src="https://img.shields.io/pypi/v/PyPgConfig?label=PyPI"></a>
<a href="https://github.com/Florents-Tselai/babar/actions/workflows/test.yml?branch=mainline"><img src="https://github.com/Florents-Tselai/PyPgConfig/actions/workflows/test.yml/badge.svg"></a>
<a href="https://codecov.io/gh/florents-tselai/PyPgConfig"><img src="https://codecov.io/gh/Florents-Tselai/PyPgConfig/branch/main/graph/badge.svg"></a>  
<a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"></a>
<a href="https://github.com/Florents-Tselai/PyPgConfig/releases"><img src="https://img.shields.io/github/v/release/Florents-Tselai/PyPgConfig?include_prereleases&label=changelog"></a>


## Installation

Install this tool using `pip`:
```bash
pip install PyPgConfig
```

## Usage

```python
from pypgconfig import detect

pgconf = detect()
pgconf.version # "15.4"
pgconf.version.major # 15
pgconf.version.minor # 4

pgconf.libs # ["pgcommon", "pgport", "lz4", "xml2" ]

pgconf.with_python # True
pgconf.pythonpath # Path("/opt/homebrew/bin/python3.11")
```

