#!/usr/bin/env python3

from .utils import normalize, lens

import argparse
from datetime import date
import os
import logging
import exifread
import csv

from PIL import Image, ImageDraw, ImageFont

original_width = 6000
original_height = 4000


def burn_exif_data(in_file, options):
    """Given an input filename and output filename, rewrites an image without EXIF data"""

    image_buffer = open(in_file, 'rb')
    exif_data = exifread.process_file(image_buffer, details=False)
    image_data = Image.open(image_buffer)

    watermark_container = Image.new(
        'RGB', [original_width, 600], (255, 255, 255)
    )

    print(os.path.dirname(__file__))

    fonts = os.path.join(
        os.path.dirname(__file__),
        'themes',
        'talk-with-kana',
        'Inter-Medium.otf'
    )

    # print(fonts)

    text_title = ImageFont.truetype(fonts, 64)
    text_normal = ImageFont.truetype(fonts, 80)

    color_title = "#00C7B1"
    color_normal = "#636363"

    exif_data = {i: x.printable for i, x in exif_data.items()}

    # print(exif_data)

    datetime = exif_data['EXIF DateTimeDigitized'].replace(":", "-", 2)
    exif_fnumber = None
    try:
        exif_fnumber = " f/{}".format(str(eval(exif_data['EXIF FNumber'])))
    except:
        exif_fnumber = ""

    text1 = "{} + {}\n{} {}s {}mm{}\nISO {}".format(
        normalize.make_model(
            exif_data['Image Make'], exif_data['Image Model']),
        lens.get_binding_of(
            normalize.make_model(
                exif_data.get('EXIF LensMake', ''), exif_data['EXIF LensModel']
            ), options
        ),
        str(exif_data['EXIF ExposureProgram']), str(exif_data['EXIF ExposureTime']), str(
            eval(exif_data['EXIF FocalLength'])), exif_fnumber,
        exif_data['EXIF ISOSpeedRatings']
    )

    draw = ImageDraw.Draw(watermark_container)
    draw.text(
        (192, 204),
        options['event_name'],
        font=text_title, fill=color_title
    )
    draw.text((192, 291), datetime, font=text_normal, fill=color_normal)

    draw.multiline_text(((watermark_container.size[0] - 192), 144), text1,
                        anchor='ra', font=text_normal, fill=color_normal, align='right')

    out_file = os.path.join(options.get('output_dir'),
                            os.path.basename(in_file))

    resize_factor = image_data.size[0]/watermark_container.size[0]

    watermark_container = watermark_container.resize(
        (int(watermark_container.size[0] * resize_factor), int(watermark_container.size[1] * resize_factor)))

    watermarked_image = Image.new(
        'RGB', (image_data.size[0], image_data.size[1] + watermark_container.size[1]), (255, 255, 255))

    watermarked_image.paste(image_data, (0, 0))
    watermarked_image.paste(watermark_container, (0, image_data.height))

    logging.info('Writing to {}'.format(out_file))
    # watermarked_image
    watermarked_image.save(
        out_file,
        'JPEG',
        quality=90,
        exif=image_data.info['exif']
    )
    image_buffer.close()


def prase_output_dir(out_dir=None, input_dir=None):
    """Builds the output directory path, defaulting to `default` under `os.getcwd()`."""
    if out_dir:
        return os.path.abspath(os.path.expanduser(out_dir))
    else:
        return os.path.join(os.getcwd(), "output")


def prase_input_dir(files=None):
    """Returns a list of input files to process"""

    print(os.path.abspath(os.path.expanduser(files[0])))
    if os.path.isfile(files[0]):
        return files[0]
    if os.path.isdir(files[0]):
        return [os.path.join(files[0], f) for f in os.listdir(files[0])]


def exifstamp():
    global prase_input_dir, prase_output_dir, burn_exif_data

    parser = argparse.ArgumentParser(
        description='strip and stamp a watermark with EXIF data from images')

    parser.add_argument('-s', '--no-strip', dest='no_strip_exif', type=bool,
                        help='do not strip EXIF data from images. default is False')
    parser.set_defaults(no_strip_exif=False)

    parser.add_argument('-t', '--theme', dest='theme', type=str,
                        help='watermark theme, default is talk-with-kana')
    parser.set_defaults(theme='talk-with-kana')

    parser.add_argument('-o', '--output', dest='output_dir', type=str,
                        metavar='OUTPUT', help='set output directory. Defaults to "./output" or input directory with prefix "_stamped"')
    parser.set_defaults(output_dir=None)

    parser.add_argument('-n', '--no-watermark', dest='no_watermark',
                        action='store_true', help='do not put watermark on images. default is False')
    parser.set_defaults(no_watermark=False)

    parser.add_argument('-e', '--event-name', dest='event_name',
                        type=str, help='Watermark Heading 1')
    parser.set_defaults(event_name='')

    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='print helpful debugging information')
    parser.set_defaults(debug=False)

    parser.add_argument('input_file', nargs='+', metavar='INPUT',
                        help='path(s) to file(s) to watermark/scrub on')

    (args, remaining) = parser.parse_known_args()

    input_files = prase_input_dir(args.input_file)
    output_dir = prase_output_dir(args.output_dir)

    level = logging.DEBUG if args.debug == True else logging.INFO
    logging.basicConfig(level=level)

    logging.debug(
        'Input file(s): {}'.format(input_files))

    logging.debug(
        'Ensuring output directory ({}) exists'.format(output_dir))
    os.makedirs(output_dir, exist_ok=True)

    options = {
        'output_dir': output_dir,
        'debug': args.debug,
        'event_name': args.event_name,
        'theme': args.theme,
        'no_watermark': args.no_watermark
    }

    for filename in input_files:
        try:
            burn_exif_data(filename, options)
        except Exception as e:
            logging.error(
                f'something went wrong with this file "{filename}": {e}')
