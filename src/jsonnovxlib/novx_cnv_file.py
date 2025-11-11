"""Provide a class for novx conversion file representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/mdnov_novx
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re

from nvlib.model.novx.novx_file import NovxFile


class NovxCnvFile(NovxFile):

    MD_REPLACEMENTS = [
        ('<em> ', ' <em>'),
        ('<strong> ', ' <strong>'),
        ('</em><em>', ''),
        ('</strong><strong>', ''),
        ('<p>', ''),
        ('<p style="quotations">', ''),
        ('</p>', '\n'),
        ('<em>', '*'),
        ('</em>', '*'),
        ('<strong>', '**'),
        ('</strong>', '**'),
        ('  ', ' '),
    ]

    def read(self):
        super().read()
        for scId in self.novel.sections:
            self._convert_sc_content_to_md(scId)
            self._adjust_viewpoint(scId)

    def write(self):
        for scId in self.novel.sections:
            self._convert_sc_content_to_xml(scId)
            self._set_viewpoint(scId)
        super().write()

    def _adjust_viewpoint(self, scId):
        # Make sure that the viewpoint character is the first in the list.
        viewpoint = self.novel.sections[scId].viewpoint
        if not viewpoint:
            return

        scCharacters = self.novel.sections[scId].characters
        if viewpoint in scCharacters:
            scCharacters.remove(viewpoint)
        scCharacters.insert(0, viewpoint)
        self.novel.sections[scId].characters = scCharacters

    def _convert_sc_content_to_md(self, scId):
        # Convert novx markup to Markdown.
        text = self.novel.sections[scId].sectionContent
        if not text:
            return

        for novx, md in self.MD_REPLACEMENTS:
            text = text.replace(novx, md)
        text = text.replace('\n', '@%&')
        text = re.sub(r'<comment>.*?</comment>', '', text)
        text = re.sub(r'<note .*?>].*?<\/note>', '', text)
        newlines = []
        lines = text.split('@%&')
        for line in lines:
            newlines.append(line.strip())
        text = '\n\n'.join(newlines)
        text = re.sub(r'<span.*?>|</span>', '', text)

        if text:
            self.novel.sections[scId].sectionContent = f'{text.strip()}\n'
        else:
            self.novel.sections[scId].sectionContent = ''

    def _convert_sc_content_to_xml(self, scId):
        # Convert Markdown to novx markup.

        text = self.novel.sections[scId].sectionContent
        if not text:
            return

        while '\n\n' in text:
            text = text.replace('\n\n', '@%&').strip()
        while '***' in text:
            text = text.replace('***', '§%§')
        text = re.sub(r'\*\*(.+?)\*\*', '<strong>\\1</strong>', text)
        text = re.sub(r'\*(.+?)\*', '<em>\\1</em>', text)
        while '§%§' in text:
            text = text.replace('§%§', '***')
        newlines = []
        for line in text.split('@%&'):
            line = f'<p>{line}</p>'
            newlines.append(line)
        text = '\n'.join(newlines)

        self.novel.sections[scId].sectionContent = text

    def _set_viewpoint(self, scId):
        # Use the first related character as a viewpoint character.
        scCharacters = self.novel.sections[scId].characters
        if scCharacters:
            self.novel.sections[scId].viewpoint = scCharacters[0]

