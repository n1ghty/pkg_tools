# pkg_tools by n1ghty
Collection of PS4 pkg tools which currently consists of pkg_list and pkg_rename.

## pkg_list
**Pkg list generator for PS4 pkg files.**

This tool parses all pkg files in the specified directory/directories recursively
and generates an excel sheet from the parsed infos.

### Usage
```
usage: pkg_list.py [-h] pkg_path [pkg_path ...] [-r] [-c COLUMN [COLUMN ...]] [-s SORT] [-d] [-o OUTFILE]

This tool parses all pkg files in the specified directory/directories recursively
and generates an excel sheet from the parsed infos.

Available values for the columns:
 Raw values from param.sfo like
  - TITLE, TITLE_ID, CONTENT_ID, VERSION, APP_VER, PARENTAL_LEVEL,
    SYSTEM_VER, ...
 Formatted values, especially for version information:
  - LANGUAGES
    The list of title name languages, e.g. 'EN,FR,RU'
    This does not always reflect supported languages.  - VER
    Equals VERSION for a game / an application and APP_VER(U) for an update
  - SYS_VER
    The required system version number in a readable format, e.g. '2.70'
  - SDK_VER
    The used sdk version number in a readable format - if available - e.g. '2.70'
  - REGION
    The region of the pkg (CN, EU, US)
  - SIZE
    The filesize in a readable format, e.g. '1.1 GB'
  - TITLE_XX
    The title name in a specific language XX. If not available, the default
    language is used.

    Available language codes:
      JA, EN, FR, ES, DE, IT, NL, PT, RU, KO, CH, ZH, FI, SV, DA,
      NO, PL, BR, GB, TR, LA, AR, CA, CS, HU, EL, RO, TH, VI, IN

positional arguments:
  pkg_path              the path(s) to scan for pkg files

optional arguments:
  -h, --help            show this help message and exit
  -r                    include subdirectories
  -c COLUMN [COLUMN ...]
                        specify the columns
  -s SORT               sort list by specific column
  -d                    use descending sorting
  -o OUTFILE            specify the output file name (without suffix)
```

## pkg_rename
**Pkg file renamer for PS4 pkg files.**

This tool renames PS4 pkg files to the sony format (default), a readable
name format or a custom specified format.

### Usage
```
usage: pkg_rename.py [-h] pkg_path [-t] [-c CUSTOM_FORMAT] [-n] [-d] [-r]

This tool renames PS4 pkg files to the sony format (default), a readable
name format or a custom specified format.

For the custom formatting, values can be replaced by surrounding them with
%-characters.
E.g. '%TITLE% (%TITLE_ID%)' will result in 'Game name (CUSA01234)'

Available values for formatting:
 Raw values from param.sfo like
  - TITLE, TITLE_ID, CONTENT_ID, VERSION, APP_VER, PARENTAL_LEVEL,
    SYSTEM_VER, ...
 Formatted values, especially for version information:
  - LANGUAGES
    The list of title name languages, e.g. 'EN,FR,RU'
    This does not always reflect supported languages.  - VER
    Equals VERSION for a game / an application and APP_VER(U) for an update
  - SYS_VER
    The required system version number in a readable format, e.g. '2.70'
  - SDK_VER
    The used sdk version number in a readable format - if available - e.g. '2.70'
  - REGION
    The region of the pkg (CN, EU, US)
  - SIZE
    The filesize in a readable format, e.g. '1.1 GB'
  - TITLE_XX
    The title name in a specific language XX. If not available, the default
    language is used.

    Available language codes:
      JA, EN, FR, ES, DE, IT, NL, PT, RU, KO, CH, ZH, FI, SV, DA,
      NO, PL, BR, GB, TR, LA, AR, CA, CS, HU, EL, RO, TH, VI, IN
The readable name format (-n) uses the following format:
'%TITLE% (%TITLE_ID%) [v%VER%]'

positional arguments:
  pkg_path          the pkg file which shall be renamed (or directory when
                    used with -d)

optional arguments:
  -h, --help        show this help message and exit
  -t                only test the formatting without renaming
  -c CUSTOM_FORMAT  custom file name format
  -n                use a readable name format
  -d                rename all files in the specified directory
  -r                include subdirectories
```

## Acknowledgements
PKG parsing is based on
- *UnPKG rev 0x00000008 (public edition), (c) flatz*

Param.sfo parsing is based on
- *Python SFO Parser by: Chris Kreager a.k.a LanThief*