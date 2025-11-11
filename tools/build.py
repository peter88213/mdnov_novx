"""Build the mdnov_novx script.

Note: VERSION must be updated manually before starting this script.
        
For further information see https://github.com/peter88213/mdnov_novx
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import search_modules
from shutil import rmtree

VERSION = '0.3.0'
PRJ_NAME = 'mdnov_novx'


def insert_version_number(source, version='unknown'):
    """Write the actual version string and make sure that Unix EOL is used."""
    with open(source, 'r', encoding='utf_8') as f:
        text = f.read().replace('@release', version)
    with open(source, 'w', encoding='utf_8', newline='\n') as f:
        f.write(text)
    print(f'Version {version} set.')


def main():
    sourceDir = '../src/'
    distDir = '../dist/'
    sourceFile = f'{sourceDir}{PRJ_NAME}_.py'
    distFile = f'{distDir}{PRJ_NAME}.py'
    try:
        rmtree(distDir)
    except FileNotFoundError:
        pass
    os.makedirs(distDir)
    search_modules.run(
        sourceFile,
        'jsonnovxlib',
        '../../mdnov_novx/src/',
        distDir
        )
    search_modules.run(
        sourceFile,
        'mdnvlib',
        '../../mdnovel/src/',
        distDir
        )
    search_modules.run(
        sourceFile,
        'nvlib',
        '../../novelibre/src/',
        distDir
        )
    insert_version_number(distFile, version=VERSION)


if __name__ == '__main__':
    main()
