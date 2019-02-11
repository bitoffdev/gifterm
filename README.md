# GifTerm

This project runs a server that allows you to render any
[GIF](https://en.wikipedia.org/wiki/GIF) in a terminal emulator using shell
commands such as `curl` or `wget`.

This project was originally created for Big Red Hacks in the Fall of 2018.

## Setup

Before continuing, make sure you have Python 3 and Pip installed.

### Optional: Use Virtual Python Environment

I recommend using [virtualenv](https://virtualenv.pypa.io). This can save you
from a lot of headaches if you have multiple python projects with many
dependencies on the same computer.

Run the following command in your favorite shell to install `virtualenv`:

```bash
python3 -m pip install --user virtualenv
```

Now, run the following commands in the root directory of this repository to
create and enter the virtual python environment:

```bash
virtualenv -p python3 env
source env/bin/activate
```

Now, you can proceed with the next step. You can get out of the virtual python
environment at anytime by running `deactivate`.

### Importing img2txt submodule

This repo uses the [img2txt](https://github.com/hit9/img2txt) submodule. Once
you have cloned this repo, run the following to import the `img2txt` git repo:

```bash
git submodule init
git submodule update
```

### Installing the dependencies with pip

```bash
python3 -m pip install -r requirements.txt
```

## Running the server

Once you are setup, run the following in the root directory of this repository:

```bash
python3 -m gifterm
```

This will start a [Flask](http://flask.pocoo.org/) server on port 5000 of your computer.

## Client usage

**Using curl**

```bash
curl localhost:5000
```

**Using wget**

```bash
wget -qO- localhost:5000
```

## Docker

If you are familiar with Docker, there is an image in this repository. You can
build and run the Docker image with the following 2 commands:

```bash
docker build -t gifterm:latest .
docker run -tip 5000:5000 gifterm
```

## Example GIFs

- [Banana Dance](https://media.giphy.com/media/IB9foBA4PVkKA/giphy.gif)
- [Party Parrot](https://media.giphy.com/media/l3q2zVr6cu95nF6O4/giphy.gif)
