#!/usr/bin/python3
"""Converter between .mdnov and .novx file format.

usage: mdnov_novx.py sourcefile

Version @release
Requires Python 3.7+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnov_novx
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import os
import sys

from jsonnovxlib.novx_cnv_file import NovxCnvFile
from mdnvlib.json.json_file import JsonFile
from nvlib.model.data.novel import Novel
from nvlib.model.data.nv_tree import NvTree
from nvlib.novx_globals import norm_path
from nvlib.alternative_ui.ui_cmd import UiCmd


class NovxConverter():

    def run(self, sourcePath):
        sourceRoot, sourceExtension = os.path.splitext(sourcePath)
        if sourceExtension == NovxCnvFile.EXTENSION:
            targetPath = f'{sourceRoot}{JsonFile.EXTENSION}'
            source = NovxCnvFile(sourcePath)
            target = JsonFile(targetPath)
        elif sourceExtension == JsonFile.EXTENSION:
            targetPath = f'{sourceRoot}{NovxCnvFile.EXTENSION}'
            source = JsonFile(sourcePath)
            target = NovxCnvFile(targetPath)
        else:
            self.ui.set_info(f'!File format "{sourceExtension}" is not supported.')
            return

        if not os.path.isfile(sourcePath):
            self.ui.set_info(f'!File not found: "{sourcePath}".')
            return

        if os.path.isfile(targetPath):
            if not self.ui.ask_yes_no(f'Overwrite existing file "{norm_path(targetPath)}"?'):
                self.ui.set_info('!Action canceled by user.')
                return

        source.novel = Novel(tree=NvTree())
        source.read()
        target.novel = source.novel
        target.wcLog = source.wcLog
        target.write()
        self.ui.set_info(f'File written: "{norm_path(targetPath)}".')


def main(sourcePath, suffix=''):
    ui = UiCmd('Converter between .mdnov and .novx file format')
    converter = NovxConverter()
    converter.ui = ui
    converter.run(sourcePath)
    ui.start()


if __name__ == '__main__':
    main(sys.argv[1])
