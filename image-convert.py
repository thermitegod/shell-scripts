#!/usr/bin/env python3
# 1.0.0
# 2020-02-25

# Copyright (C) 2020 Brandon Zorn <brandonzorn@cock.li>
#
# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3
#    as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/>.

import argparse
import os
import sys
import shutil
import tempfile
import mimetypes

from loguru import logger
from pgmagick import Image, Blob
from utils import utils


# TODO
#   fix -d flag
#   auto convert mode, maybe
#   batch support
#   size target
#   acceptable size range
#   rezizing when w > h


def convert_main(act, origext, newext, qual, size, directory, rm_orig, strip_exif, mimecheck):
    tmpdir = tempfile.mkdtemp(dir=directory)

    orig = 'orig'
    if not os.path.isdir(orig):
        os.mkdir(orig)

    if mimecheck:
        utils.run_cmd('sh -c "mime-correct -I"')

    for filename in os.listdir(directory):
        filename_base = os.path.splitext(filename)[0]
        filename_ext = os.path.splitext(filename)[1][1:]

        if check_if_image(filename):
            if act == 'convert':
                # when converting between diffrent formats, ex png to jpg, ensure
                # that no jpg images get converted alongside png images, simply
                # skip those images, unless converting between the same format
                if newext not in os.path.splitext(filename)[1] or origext == newext:
                    img = Image(filename)
                    if strip_exif:
                        img.profile("*", Blob())
                    img.quality(int(qual))
                    img.write(f'{tmpdir}/{filename_base}.{newext}')

                    os.rename(filename, f'{orig}/{filename}')
                else:
                    logger.debug(f'Skipping: {filename}')

            elif act == 'resize':
                img = Image(filename)
                if strip_exif:
                    img.profile("*", Blob())
                img.scale(size)
                img.write(f'{tmpdir}/{filename_base}.{filename_ext}')

                os.rename(filename, f'{orig}/{filename}')

    if os.path.exists(tmpdir):
        for filedone in os.listdir(tmpdir):
            filedone_ext = os.path.splitext(filedone)[1][1:]
            file_in_temp = f'{tmpdir}/{filedone}'
            file_final = f'{os.path.dirname(tmpdir)}/{os.path.splitext(filedone)[0]}.{filedone_ext}'

            logger.debug(f'Moving file: \'{file_in_temp}\' to \'{file_final}\'')
            os.rename(f'{file_in_temp}', f'{file_final}')

        logger.debug(f'Removing tempdir: {tmpdir}')
        shutil.rmtree(tmpdir)

    if os.path.exists(orig) and rm_orig:
        logger.debug(f'Removing Original: {orig}')
        shutil.rmtree(orig)


def convert_main_batch(act, origext, newext, qual, size, directory, rm_orig, strip_exif, mimecheck):
    utils.not_implemented()

    for dirs in os.listdir(directory):
        if os.path.isdir(dirs):
            convert_main(act=act, origext=origext, newext=newext, qual=qual, size=size, directory=dirs,
                         rm_orig=rm_orig, strip_exif=strip_exif, mimecheck=mimecheck)


def get_img_size(directory, print_only=True):
    for filename in os.listdir(directory):
        if check_if_image(filename):
            from pgmagick.api import Image
            img = Image(filename)
            if print_only:
                print(f'{img.width}x{img.height}')
            else:
                return img.width, img.height


def test_size(img_orig, img_new):
    new_is_smaller = False
    if os.path.isfile(img_orig) and os.path.isfile(img_new):
        logger.debug(f'filesize new  : {os.path.getsize(img_new)}')
        logger.debug(f'filesize orig : {os.path.getsize(img_orig)}')

        if os.path.getsize(img_orig) > os.path.getsize(img_new):
            new_is_smaller = True

    return new_is_smaller


def check_if_image(file):
    try:
        if 'image' in mimetypes.guess_type(file)[0]:
            return True
    except TypeError:
        pass
    return False


def get_mode(qual):
    if qual != '0':
        return 'convert'
    return 'convert_auto'


def convert_set_size(mode, get_size):
    if get_size == '1':
        size = '2400'
    elif get_size == '2':
        size = '1600'
    elif get_size == '3':
        size = '1280'
    elif get_size == '4':
        size = '980'
    elif get_size == '5':
        size = '780'
    else:
        size = get_size

    if mode == 'height':
        size = f'x{size}'

    return size


def convert_qual_check(newext, qual):
    max_qual = 0
    if newext == 'jpg':
        max_qual = 100
    elif newext == 'png':
        max_qual = 9

    if int(qual) > max_qual:
        utils.die(message=f'exiting because of invalid range for {newext}: {qual}')


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    debug = parser.add_argument_group('DEBUG')
    debug.add_argument('-L', '--loglevel', default='WARNING', metavar='LEVEL', type=str.upper,
                       choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'VERBOSE', 'DEBUG', 'TRACE'],
                       help='Levels: %(choices)s')

    general = parser.add_argument_group('GENERAL')
    general.add_argument('-d', '--directory',
                         metavar='DIRECTORY',
                         help='Directory to run in, currently non functional')
    general.add_argument('-r', '--rm-orig',
                         action='store_true',
                         help='do not keep original images')
    general.add_argument('-s', '--size',
                         action='store_true',
                         help='get image size in current directory')

    modify = parser.add_argument_group('FILE MODIFICATION')
    modify.add_argument('-e', '--no-strip-exif',
                        action='store_true',
                        help='Do not strip exif, can lead to runtime errors')
    modify.add_argument('-m', '--mimecheck',
                        action='store_true',
                        help='disable mime check and correction')

    batch = parser.add_argument_group('BATCH')
    batch.add_argument('-B', '--batch',
                       action='store_true',
                       help='batch, must come before other args')
    batch.add_argument('-b', '--batch-rm',
                       action='store_true',
                       help='batch, must come before other args, uses -r')

    resize_size = parser.add_argument_group('RESIZE, keeps aspect',
                                            '0: use value provided\n'
                                            '1: 2400\n'
                                            '2: 1600\n'
                                            '3: 1280\n'
                                            '4: 980\n'
                                            '5: 780\n')
    resize_size.add_argument('-H', '--height',
                             help='RESIZE Hight, keeps aspect')
    resize_size.add_argument('-W', '--width',
                             help='RESIZE Width, keeps aspect')

    resize_percent = parser.add_argument_group('RESIZE PERCENT')
    resize_percent.add_argument('-S', '--percent',
                                metavar='PERCENT',
                                help='Any percent')

    convert = parser.add_argument_group('CONVERT',
                                        'value of \'0\' sets auto mode\n'
                                        'quality ranges, higher is better quality, JPG: 1-100, PNG:1-9\n')
    convert.add_argument('-J', '--jpg-to-jpg',
                         metavar='SIZE',
                         help='convert jpg to jpg')
    convert.add_argument('-j', '--jpg-to-png',
                         metavar='SIZE',
                         help='convert jpg to png')
    convert.add_argument('-P', '--png-to-png',
                         metavar='SIZE',
                         help='convert png to png')
    convert.add_argument('-p', '--png-to-jpg',
                         metavar='SIZE',
                         help='convert png to jpg')
    args = parser.parse_args()

    utils.is_not_root()

    act = None
    origext = None
    newext = None
    qual = None
    size = None
    rm_orig = False
    mimecheck = True
    strip_exif = True

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    if args.directory:
        directory = args.directory
    else:
        directory = os.getcwd()

    if args.jpg_to_jpg:
        origext = 'jpg'
        newext = 'jpg'
        qual = args.jpg_to_jpg
        convert_qual_check(newext=newext, qual=qual)
        act = get_mode(qual=qual)

    if args.jpg_to_png:
        origext = 'jpg'
        newext = 'png'
        qual = args.jpg_to_png
        convert_qual_check(newext=newext, qual=qual)
        act = get_mode(qual=qual)

    if args.png_to_png:
        origext = 'png'
        newext = 'png'
        qual = args.png_to_png
        convert_qual_check(newext=newext, qual=qual)
        act = get_mode(qual=qual)

    if args.png_to_jpg:
        origext = 'png'
        newext = 'jpg'
        qual = args.png_to_jpg
        convert_qual_check(newext=newext, qual=qual)
        act = get_mode(qual=qual)

    if args.percent:
        size = f'{args.percent}%'
        act = 'resize'

    if args.width:
        size = convert_set_size(mode='width', get_size=args.width)
        act = 'resize'

    if args.height:
        utils.die(message='Height is currently disabled, use width')
        size = convert_set_size(mode='height', get_size=args.height)
        act = 'resize'

    if args.size:
        act = 'get_img_size'

    if args.batch:
        rm_orig = False
        act = 'batch'

    if args.batch_rm:
        rm_orig = True
        act = 'batch'

    if args.rm_orig:
        rm_orig = True

    if args.mimecheck:
        mimecheck = False

    if args.no_strip_exif:
        strip_exif = False

    if act == 'convert':
        convert_main(act='convert', origext=origext, newext=newext, qual=qual,
                     size=None, directory=directory, rm_orig=rm_orig, strip_exif=strip_exif,
                     mimecheck=mimecheck)

    elif act == 'convert_auto':
        pass

    elif act == 'batch':
        convert_main_batch(act='convert_auto', origext=origext, newext=newext, qual=qual,
                           size=size, directory=directory, rm_orig=rm_orig, strip_exif=strip_exif,
                           mimecheck=mimecheck)

    elif act == 'resize':
        convert_main(act='resize', origext=origext, newext=newext, qual=None,
                     size=size, directory=directory, rm_orig=rm_orig, strip_exif=strip_exif,
                     mimecheck=mimecheck)

    elif act == 'get_img_size':
        get_img_size(directory=directory)


if __name__ == '__main__':
    main()
