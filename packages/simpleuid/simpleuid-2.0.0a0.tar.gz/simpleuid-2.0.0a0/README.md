# SimpleUID (unique ID) for Python

[![GitHub releases](https://img.shields.io/github/v/release/w-kuipers/simpleUID)](https://github.com/w-kuipers/simpleUID/releases)
[![PyPI release](https://img.shields.io/pypi/v/simpleUID.svg)](https://pypi.org/project/simpleUID/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/github/last-commit/w-kuipers/simpleUID?label=last%20modified)](https://github.com/w-kuipers/simpleUID)


A simple and intuitive Python package for generating unique IDs written in Rust.

This package helps developers by bringing them some "quality of life" features. Stop rewriting the same piece of code in every project.

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#installation">Installation</a>
      <ul>
        <li><a href="#install-using-pip">Install using PIP</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#support">Support</a></li>
    <li><a href="#maintainer">Maintainer</a></li>
    <li><a href="#contributing">Contibruting</a></li>
    <li><a href="#license">License</a></li>

  </ol>
</details>

## Installation

### Install using PIP

    pip install simpleuid

Note that `pip` refers to the Python 3 package manager. In an environment where Python 2 is also present the correct command may be `pip3`.

## Usage

For a more detailed explaination, visit the [documentation](https://github.com/w-kuipers/simpleUID/wiki).

Import simpleUID:
``` bash
import simpleuid
```

Create a random string with letters and numbers:
``` python
simpleuid.alphanumeric()
```

Or just letters:
``` python
simpleuid.alpha()
```

or just numbers:
``` python
simpleuid.numeric()
```

You can specify the string length and a prefix:
``` python
simpleuid.alphanumeric(length=20, prefix='start')
```

Methods `alphanumeric` and `alpha` allow you the choice for only `uppercase` or `lowercase` characters. The default for this is `all`.
``` python
simpleuid.alphanumeric(case="all") ## Both UPPERCASE and lowercase (default)
simpleuid.alphanumeric(case="upper") ## ONLY UPPERCASE
simpleuid.alphanumeric(case="lower") ## only lowercase
```

All functions are:
Function        | Functionality 
------------- | -----
[alphanumeric](https://github.com/w-kuipers/simpleuid/wiki/usage#alphanumeric)       | Generates a random string containing both letters and numbers. 
[alpha](https://github.com/w-kuipers/simpleuid/wiki/usage#alpha) | Generates a random string containing only letters. 
[numeric](https://github.com/w-kuipers/simpleuid/wiki/usage#numeric)  | Generates a random string containing only numbers |
[var](https://github.com/w-kuipers/simpleuid/wiki/usage#var) | Generates a string based on a variable string provided by the user
## Support

If you found a problem with the software, please [create an issue](https://github.com/w-kuipers/simpleUID/issues) on GitHub.

## Maintainer

This project is maintained by [Wibo Kuipers](https://github.com/w-kuipers).

## Contributing

Your contributions are highly appreciated. Please [create a pull request](https://github.com/w-kuipers/simpleUID/pulls) on GitHub. Bigger changes need to be discussed with the development team via the [issues section at GitHub](https://github.com/w-kuipers/simpleUID/issues) first.


## License

[MIT LICENSE](https://github.com/w-kuipers/simpleUID/blob/master/LICENSE)

