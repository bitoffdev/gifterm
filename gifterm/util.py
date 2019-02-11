#!/usr/bin/env false
import sys
import logging
from PIL import Image

sys.path.insert(0, 'img2txt')
import ansi

logger = logging.getLogger(__name__)


def resize_image(img, antialias, maxLen, aspectRatio):
    assert isinstance(img, Image.Image)

    if aspectRatio is None:
        aspectRatio = 1.0

    # force image to RGBA - deals with palettized images (e.g. gif) etc.
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # need to change the size of the image?
    if maxLen is not None or aspectRatio != 1.0:

        native_width, native_height = img.size

        new_width = native_width
        new_height = native_height

        # First apply aspect ratio change (if any) - just need to adjust one
        # axis so we'll do the height.
        if aspectRatio != 1.0:
            new_height = int(float(aspectRatio) * new_height)

        # Now isotropically resize up or down (preserving aspect ratio) such
        # that longer side of image is maxLen
        if maxLen is not None:
            rate = float(maxLen) / max(new_width, new_height)
            new_width = int(rate * new_width)
            new_height = int(rate * new_height)

        if native_width != new_width or native_height != new_height:
            img = img.resize((new_width, new_height), Image.ANTIALIAS if
                             antialias else Image.NEAREST)

    return img


def analyse_image(bytesio):
    """
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.

    .. note::
        Sourced from https://gist.github.com/BigglesZX/4016539
    """
    im = Image.open(bytesio)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


def process_image(bytesio):
    """
    Return a generator which yields the frames of a provided GIF one at a time

    .. note::
        Sourced from https://gist.github.com/BigglesZX/4016539
    """
    mode = analyse_image(bytesio)['mode']

    im = Image.open(bytesio)

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')

    try:
        while True:
            logger.info("Yielding frame #{} of GIF using {} mode".format(i,
                        mode))

            # If the GIF uses local colour tables, each frame will have its own
            # palette. If not, we need to apply the global palette to the new
            # frame.
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)
            assert isinstance(new_frame, Image.Image)

            # Is this file a "partial"-mode GIF where frames update a region of
            # a different size to the entire image?
            # If so, we need to construct the new frame by pasting it on top of
            # the preceding frames.
            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0, 0), im.convert('RGBA'))
            yield new_frame

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass
