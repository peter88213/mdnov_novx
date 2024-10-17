# mdnov_novx

Converter between .mdnov and .novx file format.

This is a command line tool for migrating novel projects between 
[mdnovel](https://github.com/peter88213/mdnovel) and
[novelibre](https://github.com/peter88213/novelibre).

## Requirements

- A Python installation (version 3.6 or newer).

## Download

Save the file [mdnov_novx.py](https://raw.githubusercontent.com/peter88213/mdnov_novx/main/dist/mdnov_novx.py).

## Usage 

`mdnov_novx.py sourcefile`

- *novelibre* project files with the extension *.novx* are converted to *.mdnov* format.
- *mdnovel* project files with the extension *.mdnov* are converted to *.novx* format.

**Note:** Since *novelibre* and *mdnovel* do not have the same set of features, 
information may be lost during the conversion process. 

- *mdnov_novx* supports `**strong**` and `*emphasized*` highlighting in CommonMarks style. 
  Other formatting is not converted. 
- *novx* language information, comments, footnotes, and endnotes are lost. 

## License

This is Open Source software, and *mdnov_novx* is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/mdnovel/blob/main/LICENSE) file.


