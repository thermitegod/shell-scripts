# -*- coding: utf-8 -*-
# 2.12.0
# 2021-04-29

# Copyright (C) 2020,2021 Brandon Zorn <brandonzorn@cock.li>
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
import shutil
import sys
import tempfile
from pathlib import Path

from loguru import logger
from pgmagick import Blob, Image

from python.utils.execute import Execute
from python.utils.mimecheck import Mimecheck


# TODO
#   fix -d flag
#   auto convert mode, maybe
#   batch support
#   size target
#   acceptable size range
#   rezizing when w > h

class Convert:
    def __init__(self, args: argparse = None):
        self.__origext = None
        self.__newext = None
        self.__act = None
        self.__qual = None
        self.__size = None
        self.__directory = None
        self.__rm_orig = False
        self.__mimecheck = True
        self.__strip_exif = True

        self.run(args=args)

    @staticmethod
    def test_size(img_orig, img_new):
        if Path.is_file(img_orig) and Path.is_file(img_new):
            img_size_new = Path.stat(img_new).st_size
            img_size_orig = Path.stat(img_orig).st_size
            logger.debug(f'filesize new  : {img_size_new}')
            logger.debug(f'filesize orig : {img_size_orig}')

            if img_size_orig > img_size_new:
                return True

        return False

    @staticmethod
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

    def get_img_size(self, print_only=True):
        # pgmagick.api.Image is imported here to avoid name collision with
        # pgmagick.Image
        from pgmagick.api import Image

        for filename in Path(self.__directory).iterdir():
            if Mimecheck.check_if_image(filename=filename):
                img = Image(str(filename))
                if print_only:
                    print(f'{img.width}x{img.height}')
                else:
                    return img.width, img.height

    def convert_qual_check(self):
        max_qual = 0
        if self.__newext == 'jpg':
            max_qual = 100
        elif self.__newext == 'png':
            max_qual = 9

        if self.__qual > max_qual:
            logger.critical(f'exiting because of invalid range for {self.__newext}: {self.__qual}')
            raise SystemExit(1)

    def get_mode(self):
        if self.__qual != 0:
            return 'convert'
        return 'convert_auto'

    def convert_main(self):
        tmpdir = tempfile.mkdtemp(dir=self.__directory)

        orig = Path('orig')
        if not Path.is_dir(orig):
            orig.mkdir(parents=True, exist_ok=True)

        c1 = 0
        c2 = 0

        if self.__mimecheck:
            Execute('mime-correct')

        for filename in Path(self.__directory).iterdir():
            if Mimecheck.check_if_image(filename=filename):
                c1 += 1

                filename_basename = Path(filename).name
                filename_base = Path(filename).stem
                filename = str(filename)

                if self.__act == 'convert':
                    # when converting between diffrent formats, ex png to jpg, ensure
                    # that no jpg images get converted alongside png images, simply
                    # skip those images, unless converting between the same format
                    if self.__newext not in Path(filename).suffix or self.__origext == self.__newext:
                        img = Image(filename)
                        if self.__strip_exif:
                            img.profile("*", Blob())
                        img.quality(self.__qual)
                        img.write(f'{tmpdir}/{filename_base}.{self.__newext}')

                        Path.rename(Path(filename), Path() / orig / filename_basename)
                    else:
                        logger.debug(f'Skipping: {filename}')

                elif self.__act == 'resize':
                    img = Image(filename)
                    if self.__strip_exif:
                        img.profile("*", Blob())
                    img.scale(self.__size)
                    img.write(f'{tmpdir}/{str(filename_basename)}')

                    Path.rename(Path(filename), Path() / orig / filename_basename)

        if Path.exists(Path(tmpdir)):
            for filedone in Path(tmpdir).iterdir():
                filedone = Path(filedone)
                file_in_temp = Path() / tmpdir / filedone
                file_final = Path() / Path(tmpdir).parent / Path(filedone).name

                logger.debug(f'Moving file: \'{file_in_temp}\' to \'{file_final}\'')
                Path.rename(file_in_temp, file_final)

            logger.debug(f'Removing tempdir: {tmpdir}')
            shutil.rmtree(tmpdir)

        if Path.exists(orig) and self.__rm_orig:
            logger.debug(f'Removing Original: {orig}')
            shutil.rmtree(orig)

        for filename in Path(self.__directory).iterdir():
            if Mimecheck.check_if_image(filename=filename):
                c2 += 1

        if c1 != c2:
            logger.error(f'total file count does not match: {c1}, {c2} in \'{self.__directory}\'')

    def convert_main_batch(self):
        # TODO - Not Implemented

        for dirs in Path(self.__directory).iterdir():
            if Path.is_dir(Path(dirs)):
                self.convert_main()

    def run(self, args):
        if args.directory:
            self.__directory = args.directory
        else:
            self.__directory = Path.cwd()

        if args.jpg_to_jpg:
            self.__origext = 'jpg'
            self.__newext = 'jpg'
            self.__qual = args.jpg_to_jpg
            self.convert_qual_check()
            self.__act = self.get_mode()

        if args.jpg_to_png:
            self.__origext = 'jpg'
            self.__newext = 'png'
            self.__qual = args.jpg_to_png
            self.convert_qual_check()
            self.__act = self.get_mode()

        if args.png_to_png:
            self.__origext = 'png'
            self.__newext = 'png'
            self.__qual = args.png_to_png
            self.convert_qual_check()
            self.__act = self.get_mode()

        if args.png_to_jpg:
            self.__origext = 'png'
            self.__newext = 'jpg'
            self.__qual = args.png_to_jpg
            self.convert_qual_check()
            self.__act = self.get_mode()

        if args.percent:
            self.__size = f'{args.percent}%'
            self.__act = 'resize'

        if args.width:
            self.__size = self.convert_set_size(mode='width', get_size=args.width)
            self.__act = 'resize'

        if args.height:
            print('Height is currently disabled, use width')
            raise SystemExit(1)

            # self.__size = self.convert_set_size(mode='height', get_size=args.height)
            # self.__act = 'resize'

        if args.size:
            self.__act = 'get_img_size'

        if args.batch:
            self.__rm_orig = False
            self.__act = 'batch'

        if args.batch_rm:
            self.__rm_orig = True
            self.__act = 'batch'

        if args.rm_orig:
            self.__rm_orig = True

        if args.mimecheck:
            self.__mimecheck = False

        if args.no_strip_exif:
            self.__strip_exif = False

        if self.__act == 'convert':
            self.convert_main()

        elif self.__act == 'convert_auto':
            raise NotImplementedError

        elif self.__act == 'batch':
            raise NotImplementedError

        elif self.__act == 'resize':
            self.convert_main()

        elif self.__act == 'get_img_size':
            self.get_img_size()


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    general = parser.add_argument_group('general')
    general.add_argument('-d', '--directory',
                         metavar='DIRECTORY',
                         nargs=1,
                         help='Directory to run in, currently non functional')
    general.add_argument('-r', '--rm-orig',
                         action='store_true',
                         help='do not keep original images')
    general.add_argument('-s', '--size',
                         action='store_true',
                         help='get image size in current directory')

    modify = parser.add_argument_group('file modification')
    modify.add_argument('-e', '--no-strip-exif',
                        action='store_true',
                        help='Do not strip exif, can lead to runtime errors')
    modify.add_argument('-m', '--mimecheck',
                        action='store_true',
                        help='disable mime check and correction')

    batch = parser.add_argument_group('batch')
    batch.add_argument('-B', '--batch',
                       action='store_true',
                       help='batch, must come before other args')
    batch.add_argument('-b', '--batch-rm',
                       action='store_true',
                       help='batch, must come before other args, uses -r')

    resize_size = parser.add_argument_group('resize, keeps aspect',
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

    resize_percent = parser.add_argument_group('resize percent')
    resize_percent.add_argument('-S', '--percent',
                                metavar='PERCENT',
                                nargs=1,
                                type=int,
                                help='Any percent')

    convert = parser.add_argument_group('convert',
                                        'value of \'0\' sets auto mode\n'
                                        'quality ranges, higher is better quality, JPG: 1-100, PNG:1-9\n')
    convert.add_argument('-J', '--jpg-to-jpg',
                         metavar='SIZE',
                         nargs=1,
                         type=int,
                         help='convert jpg to jpg')
    convert.add_argument('-j', '--jpg-to-png',
                         metavar='SIZE',
                         nargs=1,
                         type=int,
                         help='convert jpg to png')
    convert.add_argument('-P', '--png-to-png',
                         metavar='SIZE',
                         nargs=1,
                         type=int,
                         help='convert png to png')
    convert.add_argument('-p', '--png-to-jpg',
                         metavar='SIZE',
                         nargs=1,
                         type=int,
                         help='convert png to jpg')

    debug = parser.add_argument_group('debug')
    debug.add_argument('-L', '--loglevel',
                       default='INFO',
                       metavar='LEVEL',
                       type=str.upper,
                       choices=['NONE', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'VERBOSE', 'DEBUG', 'TRACE'],
                       help='Levels: %(choices)s')

    args = parser.parse_args()

    logger.remove()
    logger.add(sys.stdout, level=args.loglevel, colorize=True)

    Convert(args=args)
