# Color Histogram

A simple Tropofy app for making a colour histogram for a web image

## Installation

First make a Python 2 virtual environment. 

After that do the following

```
git clone https://github.com/jack775544/color-histogram
cd color-histogram
git update-index --assume-unchanged development.ini
pip install -r requirements.txt
python setup.py develop
```
The pip install is not strictly required, however setup.py installs the packages from source where the pip does some pre compilation magic

The git update-index is to make sure your development key is not added to the repo

In development.ini make sure to place your Tropofy developer key into `custom.license_key` field

## Running

Execute the following command in the color-histogram directory whilst using the
virtual environment

```
tropofy_run
```

And then navigate to localhost:8080, where the app will be served to your computer 