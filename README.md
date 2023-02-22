# DjangoRoid-Server
와플스튜디오 와커톤 장고로이드 서버 리포지토리입니다. 

![](coverage.svg)
[![Python 3.8.13](https://img.shields.io/badge/python-3.8.13-blue.svg)](https://www.python.org/downloads/release/python-3813/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## Prerequisite
To setup virtualenv, follow below commands. (It is based on pyenv, but it is also fine to use conda or other virtualenv tools)
``` bash
$ pyenv install 3.8.13
$ pyenv virtualenv 3.8.13 DjangoRoid
$ pyenv activate DjangoRoid
$ pip install -r requirements.txt
```

To apply precommit hook, please execute below command in terminal.

``` bash
$ yarn install
```

If you are using window os, perform the following command before every commit:
``` bash
$ sh dos2unix.sh
```


## Convention
- [Python Google Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Black](https://black.readthedocs.io/en/stable/)
- [Isort](https://pycqa.github.io/isort/)

## API Documentation
- [DjangoRoid API Doc](https://historical-garage-3bd.notion.site/DjangoRoid-API-Documentation-eba8908c20164559b8544e8d554d5df8)
