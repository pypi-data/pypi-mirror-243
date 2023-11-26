# mediagrab
Python CLI to download videos from youtube

[![PyPI - Version](https://img.shields.io/pypi/v/mediagrab)](https://pypi.org/project/mediagrab/0.0.7)
[![PyPI - License](https://img.shields.io/pypi/l/mediagrab)](LICENSE)

## Installation
You can install the package using following command:
```sh
pip3 install mediagrab
```
(or)
```sh
pip install mediagrab
```

## Usage

### Getting help with command line arguments
```sh
mediagrab --help
```

### Main functionality
```
usage: mediagrab [-h] [-d DESTINATION] url

positional arguments:
  url                   URL of video on YouTube to download

options:
  -h, --help            show this help message and exit
  -d DESTINATION, --destination DESTINATION
                        destination path
```

## Development setup
Clone this repository and install packages listed in requirements.txt
```sh
pip3 install -r requirements.txt
```