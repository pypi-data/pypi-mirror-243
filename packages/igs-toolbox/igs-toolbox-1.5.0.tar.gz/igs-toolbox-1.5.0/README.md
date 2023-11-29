# igs-toolbox

## Description
This Python package contains tools to check whether files follow predefined schemas of the IGS project.
Currently, only a JSON validator is implemented, but the idea is that it will be extended to more applications related to the IGS project in the future.

## Installation 

igs-toolbox is installable using pip.

```bash
pip install igs-toolbox
```

## Usage
All tools can be used directly through the commandline.

### jsonChecker

```bash
usage: jsonChecker [-h] -i INPUT 

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Filepath to json file.
```

### readQR

The method readQR reads the Meldungsquittung and extracts the MeldungsID. 

Poppler is required to read the pdfs
```bash
conda install poppler
or
mamba install poppler
or
apt install poppler-utils
```


```bash
usage: readQR [-h] [--version] [file ...]

positional arguments:
  file

options:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

Example:
```bash
readQR *.pdf
```
