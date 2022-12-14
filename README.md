# EXIFMark

Adobe Lightroom's built-in watermarking tools not good enough. Why I don't make it yourself?

## installation

## install from source

## usage

```
$ exifstamp -h
usage: exifstamp [-h] [-s NO_STRIP_EXIF] [-t THEME] [-o OUTPUT] [-n] [-e EVENT_NAME] [--debug] INPUT [INPUT ...]

strip and stamp a watermark with EXIF data from images

positional arguments:
  INPUT                 path(s) to file(s) to watermark/scrub on

options:
  -h, --help            show this help message and exit
  -s NO_STRIP_EXIF, --no-strip NO_STRIP_EXIF
                        do not strip EXIF data from images. default is False
  -t THEME, --theme THEME
                        watermark theme, default is talk-with-kana
  -o OUTPUT, --output OUTPUT
                        set output directory. Defaults to "./output" or input directory with prefix "_stamped"
  -n, --no-watermark    do not put watermark on images. default is False
  -e EVENT_NAME, --event-name EVENT_NAME
                        Watermark Heading 1
  --debug               print helpful debugging information
```
