"""Converter between .mdnov and .novx file format.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnov_novx
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
import os
import sys

from mdnvlib.converter.ui_cmd import UiCmd
from mdnvlib.mdnov.mdnov_file import MdnovFile
from mdnvlib.model.novel import Novel
from mdnvlib.model.nv_tree import NvTree
from mdnvlib.novx_globals import norm_path
from novxlib.novx_file import NovxFile


class NovxConverter():

    def run(self, sourcePath):
        if not os.path.isfile(sourcePath):
            return

        sourceRoot, sourceExtension = os.path.splitext(sourcePath)
        if sourceExtension == NovxFile.EXTENSION:
            targetPath = f'{sourceRoot}{MdnovFile.EXTENSION}'
            source = NovxFile(sourcePath)
            target = MdnovFile(targetPath)
        elif sourceExtension == MdnovFile.EXTENSION:
            targetPath = f'{sourceRoot}{NovxFile.EXTENSION}'
            source = MdnovFile(sourcePath)
            target = NovxFile(targetPath)
        if os.path.isfile(targetPath):
            if not self.ui.ask_yes_no(f'Overwrite existing file "{norm_path(targetPath)}"?'):
                self.ui.set_status('!Action canceled by user.')
                return

        source.novel = Novel(tree=NvTree())
        source.read()
        target.novel = source.novel
        target.write()
        self.ui.set_info_how(f'File written: "{norm_path(targetPath)}"')


def main(sourcePath, suffix=''):
    ui = UiCmd('Converter between .mdnov and .novx file format')
    converter = NovxConverter()
    converter.ui = ui
    converter.run(sourcePath)
    ui.start()


if __name__ == '__main__':
    main(sys.argv[1])
