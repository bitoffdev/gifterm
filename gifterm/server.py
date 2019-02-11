#!/usr/bin/env false
import sys
import io
import requests
import time
from flask import Flask, Response, request
from .util import resize_image
from .util import process_image

sys.path.insert(0, 'img2txt')
import ansi

app = Flask(__name__)

# https://en.wikipedia.org/wiki/ANSI_escape_code#CSI_sequences
# All sequences start with ESC (27 / hex 0x1B / octal 033).
CSI = '\033['
CSI_ERASE = CSI + '2J'
CSI_SGR_BG = CSI + '49m'    # default background color
CSI_SGR_RESET = CSI + '0m'  # reset SGR

# default gif
DEFAULT_GIF = "https://ph-files.imgix.net/caf5608a-67ec-4f9f-acb5-db0052c33bed"


def looper(iterator, count):
    """
    loop over an iterator `count` times by memorizing the iterator the first
    time through
    """
    memoize = list()
    try:
        while True:
            nex = next(iterator)
            memoize.append(nex)
            yield nex
    except StopIteration:
        while count > 0:
            for elem in memoize:
                yield elem
            count -= 1


@app.route('/')
def ascii_gif():
    def generate(bytesio):
        assert isinstance(bytesio, io.BytesIO)
        for frame in looper(process_image(bytesio), 3):
            img = resize_image(frame, antialias=False, maxLen=50.0,
                               aspectRatio=1.0)
            pixel = img.load()
            width, height = img.size

            yield CSI_SGR_BG + CSI_ERASE + \
                ansi.generate_ANSI_from_pixels(pixel, width, height, None)[0]
            time.sleep(0.05)

        yield CSI_SGR_BG + CSI_ERASE + CSI_SGR_RESET + "\n"

    # load the image
    url = request.args.get('url', DEFAULT_GIF)
    bytesio = io.BytesIO(requests.get(url).content)

    return Response(generate(bytesio), mimetype='text')
