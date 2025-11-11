"""Build a Python script for a mdnvlib based application.
        
In order to distribute single scripts without dependencies, 
this script "inlines" all modules imported from the mdnvlib package.

- Discards docstrings and multiline strings in double quotes.
- Discards comment lines.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mdnov_novx
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re
import os
from shutil import copyfile

PROJECT = 'mdnov_novx'


def search_module(modulePath, package, packagePath, distDir, processedModules):
    print(f'Processing "{modulePath}"...')
    target = modulePath.replace(f'/../{PROJECT}', '')
    targetDir = distDir + package
    os.makedirs(targetDir, exist_ok=True)
    print(target)
    if not os.path.isfile(target):
        copyfile(modulePath, target)
    with open(modulePath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # document parsing always starts in the header
    inDocstring = False
    for line in lines:
        if line.startswith('# do_not_inline'):
            break

        if line.count('"""') == 2:
            # Discard single-line docstring.
            continue

        if line.lstrip().startswith('#'):
            if not line.lstrip().startswith('#!'):
                # Discard comment line, but keep the shebang.
                continue

        if line.count('"""') == 1:
            # Beginning or end of a multi-line docstring
            if package in modulePath:
                # This is not the root script
                # so discard the module's docstring
                if inDocstring:
                    # docstring ends
                    inDocstring = False
                else:
                    # docstring begins
                    inDocstring = True
        elif not inDocstring:
            if package in modulePath:
                if 'main()' in line:
                    return

                if '__main__' in line:
                    return

            if 'import ' in line:
                importModule = re.match(r'from (.+?) import.+', line)
                if (importModule is not None) and (package in importModule.group(1)):
                    packageName = re.sub(r'\.', r'\/', importModule.group(1))
                    moduleName = f'{packagePath}{packageName}'
                    if not (moduleName in processedModules):
                        processedModules.append(moduleName)
                        search_module(
                            f'{moduleName}.py',
                            package,
                            packagePath,
                            distDir,
                            processedModules
                        )
                elif line.lstrip().startswith('import'):
                    moduleName = line.replace('import ', '').rstrip()
                    if not (moduleName in processedModules):
                        processedModules.append(moduleName)


def run(sourceFile, package, packagePath, distDir):
    processedModules = []
    search_module(sourceFile, package, packagePath, distDir, processedModules)
