# Bibtex Autocomplete

[![PyPI version][version-shield]][pypi-link]
[![PyPI pyversions][pyversion-shield]][pypi-link]
[![License][license-shield]](https://choosealicense.com/licenses/mit/)
[![PyPI status][status-shield]][pypi-link]
[![Downloads][download-shield]](https://pepy.tech/project/bibtexautocomplete)

[![Maintenance][maintain-shield]][commit-link]
[![Commit][commit-shield]][commit-link]
[![actions][pipeline-shield]][pipeline-link]
[![issues][issues-shield]][issues-link]
[![pull requests][pr-shield]][pr-link]

[version-shield]:   https://img.shields.io/pypi/v/bibtexautocomplete.svg
[pyversion-shield]: https://img.shields.io/pypi/pyversions/bibtexautocomplete.svg
[license-shield]:   https://img.shields.io/pypi/l/bibtexautocomplete.svg
[status-shield]:    https://img.shields.io/pypi/status/bibtexautocomplete.svg
[download-shield]:  https://static.pepy.tech/badge/bibtexautocomplete
[pypi-link]: https://pypi.python.org/pypi/bibtexautocomplete/

[maintain-shield]: https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg
[commit-shield]: https://img.shields.io/github/last-commit/dlesbre/bibtex-autocomplete
[commit-link]: https://github.com/dlesbre/bibtex-autocomplete/graphs/commit-activity

[pipeline-shield]: https://img.shields.io/github/actions/workflow/status/dlesbre/bibtex-autocomplete/python-app.yml?branch=master&label=tests
[pipeline-link]: https://github.com/dlesbre/bibtex-autocomplete/actions/workflows/python-app.yml

[issues-shield]: https://img.shields.io/github/issues/dlesbre/bibtex-autocomplete
[issues-link]: https://github.com/dlesbre/bibtex-autocomplete/issues

[pr-shield]: https://img.shields.io/github/issues-pr/dlesbre/bibtex-autocomplete
[pr-link]: https://github.com/dlesbre/bibtex-autocomplete/pulls

**bibtexautocomplete** or **btac** is a simple script to autocomplete BibTeX
bibliographies. It reads a BibTeX file and looks online for any additionnal data
to add to each entry. If you have a bibliography that is missing DOI information
or want to add URLs to your entries, then `btac` might be able to help. You can also
use it to quickly generate BibTeX entries from minimal data (e.g. just a title).

It is inspired and expanding on the solution provided by
[thando](https://tex.stackexchange.com/users/182467/thando) in this
[TeX stack exchange post](https://tex.stackexchange.com/questions/6810/automatically-adding-doi-fields-to-a-hand-made-bibliography).

It attempts to complete a BibTeX file by querying the following domains:
- [www.crossref.org](https://www.crossref.org/)
- [arxiv.org](https://arxiv.org/)
- [semanticscholar.org](https://www.semanticscholar.org/)
- [dblp.org](https://dblp.org)
- [researchr.org](https://researchr.org/)
- [unpaywall.org](https://unpaywall.org/)

Big thanks to all of them for allowing open, easy and well-documented access to
their databases.

**Contents:**

- [Demo](#demo)
- [Quick overview](#quick-overview)
- [Installation](#installation)
  - [Dependencies](#dependencies)
- [Usage](#usage)
- [Command line arguments](#command-line-arguments)
  - [Query filtering](#query-filtering)
  - [Output formatting](#output-formatting)
  - [Optional flags](#optional-flags)

## Demo

![demo.svg](https://raw.githubusercontent.com/dlesbre/bibtex-autocomplete/2d1a01f5ec94c8af9c2f3c1a810eca51bb4cce74/imgs/demo.svg)

## Quick overview

**How does it find matches?**

`btac` queries the websites using the entry DOI (if known) or its title. So
entries that don't have one of those two fields *will not* be completed.
- DOIs are only used if they can be recognized, so the `doi` field should
  contain "10.xxxx/yyyy" or an URL ending with it.
- Titles should be the full title. They are compared excluding case and
  punctuation, but titles with missing words will not match.
- If one or more authors are present, entries with no common authors will not
  match. Authors are compared using lower case last names only. Be sure to use
  one of the correct BibTeX formats for the author field:
  ```bibtex
  author = {First Last and Last, First and First von Last}
  ```
  (see
  [https://www.bibtex.com/f/author-field/](https://www.bibtex.com/f/author-field/)
  for full details)
- If the year is known, entries with different years will also not match.

**Disclaimers**

- There is no guarantee that the script will find matches for your entries, or
  that the websites will have any data to add to your entries, (or even that the
  website data is correct, but that's not for me to say...)

- The script is designed to minimize the chance of false positives - that is
  adding data from another similar-ish entry to your entry. If you find any such
  false positive please report them using the [issue
  tracker](https://github.com/dlesbre/bibtex-autocomplete/issues).

**How are entries completed?**

Once responses from all websites have been found, the script will add fields
from website with the following priority :

crossref > arxiv > semantic scholar > dblp > researchr > unpaywall.

So if both crossref's and dblp's response contain a publisher, the one from
crossref will be used. This order can be changed using the `-q --only-query`
option (see [query filtering](#query-filtering)).

The script will not overwrite any user given non-empty fields, unless the
`-f/--force-overwrite` flag is given. If you want to check what fields are
added, you can use `-v/--verbose` to have them printed to stdout (with
source information), or `-p/--prefix` to have the new fields be prefixed with
`BTAC` in the output file.

The script checks that the DOIs or URLs found correspond (or redirect to) a
valid webpage before adding them to an entry.

## Installation

Can be installed with [pip](https://pypi.org/project/pip/) :

```console
pip install bibtexautocomplete
```

You should now be able to run the script using either command:

```console
btac --version
python3 -m bibtexautocomplete --version
```

### Dependencies

This package has two dependencies (automatically installed by pip) :

- [bibtexparser](https://bibtexparser.readthedocs.io/)
- [alive_progress](https://github.com/rsalmei/alive-progress) (>= 3.0.0) for the fancy progress bar

## Usage

The command line tool can be used as follows:
```console
btac [--flags] <input_files>
```

**Examples :**

- `btac my/db.bib` : reads from `./my/db.bib`, writes to `./my/db.btac.bib`.
  A different output file can be specified with `-o`.
- `btac -i db.bib` : reads from `db.bib` and overwrites it (inplace flag)
- `btac folder` : reads from all files ending with `.bib` in folder. Excludes
  `.btac.bib` files unless they are the only `.bib` files present. Writes to
  `folder/file.btac.bib` unless inplace flag is set.
- `btac` with no inputs is same as `btac .`, reads file from current working directory
- `btac -c doi ...` only completes DOI fields, leave others unchanged
- `btac -v ...` verbose mode, pretty prints all new fields when done

**Note:** the [parser](https://pypi.org/project/bibtexparser/) doesn't preserve
format information, so this script will reformat your files. Some [formatting
options](#output-formatting) are provided to control output format.

**Slow responses:** I found that crossref responds significantly slower than the
other websites. It often takes longer than the 20s timeout.
- You can increase timeout with `btac ... -t 60` (60s) or `btac ... -t -1` (no timeout)
- You can disable crossref queries with `btac ... -Q crossref`

## Command line arguments

- `-o --output <file.bib>`

  Write output to given file. Can be used multiple times when also giving
  multiple inputs. Maps inputs to outputs in order. If there are extra inputs,
  uses default name (`old_name.btac.bib`). Ignored in inplace (`-i`) mode.

  For example `btac db1.bib db2.bib db3.bib -o out1.bib -o out2.bib` reads `db1.bib`,
  `db2.bib` and `db3.bib`, and write their outputs to `out1.bib`, `out2.bib`
  and `db3.btac.bib` respectively.

### Query filtering

- `-q --only-query <site>` or `-Q --dont-query <site>`

  Restrict which websites to query from. `<site>` must be one of: `crossref`,
  `arxiv`, `s2`, `dblp`, `researchr`, `unpaywall`. These arguments can be used
  multiple times, for example to only query crossref and dblp use `-q crossref
  -q dblp` or `-Q researchr -Q unpaywall -Q arxiv -Q s2`

  Additionally, you can use `-q` to change the completion priority.
  So `-q unpaywall -q researchr -q dblp -q s2 -q arxiv -q crossref` reverses the
  default order.

- `-e --only-entry <id>` or `-E --exclude-entry <id>`

  Restrict which entries should be autocompleted. `<id>` is the entry ID used in
  your BibTeX file (e.g. `@inproceedings{<id> ... }`). These arguments can also
  be used multiple times to select only/exclude multiple entries

- `-c --only-complete <field>` or `-C --dont-complete <field>`

  Restrict which fields you wish to autocomplete. Field is a BibTeX field (e.g.
  `author`, `doi`,...). So if you only wish to add missing DOIs use `-c doi`.

- `-w --overwrite <field>` or `-W --dont-overwrite <field>`

  Force overwriting of the selected fields. If using `-W author -W journal`
  your force overwrite of all fields except `author` and `journal`. The
  default is to override nothing (only complete absent and blank fields).

  For a more complex example `btac -C doi -w author` means complete all fields
  save DOI, and only overwrite author fields

  You can also use the `-f` flag to overwrite everything or the `-p` flag to add
  a prefix to new fields, thus avoiding overwrites.

- `-m --mark` and `-M --ignore-mark`

  This is useful to avoid repeated queries if you want to run `btac` many times
  on the same (large) file.

  By default, `btac` ignores any entry with a `BTACqueried` field. `--ignore-mark`
  overrides this behavior.

  When `--mark` is set, `btac` adds a `BTACqueried = {yyyy-mm-dd}` field to each entry
  it queries.

### Output formatting

Unfortunately [bibtexparser](https://pypi.org/project/bibtexparser/) doesn't
preserve format information, so this script will reformat your BibTeX file. Here
are a few options you can use to control the output format:

- `--fa --align-values` pad field names to align all values

  ```bibtex
  @article{Example,
    author = {Someone},
    doi    = {10.xxxx/yyyyy},
  }
  ```

- `--fc --comma-first` use comma first syntax

  ```bibtex
  @article{Example
    , author = {Someone}
    , doi = {10.xxxx/yyyyy}
    ,
  }
  ```

- `--fl --no-trailing-comma` don't add the last trailing comma
- `--fi --indent <space>` space used for indentation, default is a tab.
  Can be specified as a number (number of spaces) or a string with spaces
  and `_`, `t`, and `n` characters to mark space, tabs and newlines.

### Optional flags

- `-i --inplace` Modify input files inplace, ignores any specified output files
- `-p --prefix` Write new fields with a prefix. The script will add `BTACtitle =
  ...` instead of `title = ...` in the bib file. This can be combined with `-f`
  to safely show info for already present fields.

  Note that this can overwrite existing fields starting with `BTACxxxx`, even
  without the `-f` option.
- `-f --force-overwrite` Overwrite already present fields. The default is to
  overwrite a field only if it is empty or absent
- `-t --timeout <float>` set timeout on request in seconds, default: 20.0 s,
  increase this if you are getting a lot of timeouts. Set it to -1 for no timeout.
- `-S --ignore-ssl` bypass SSL verification. Use this if you encounter the error:
  ```
  [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1129)
  ```
  Another (better) fix for this is to run `pip install --upgrade certifi` to update python's certificates.

- `-d --dump-data <file.json>` writes matching entries to the given JSON files.

  This allows to see duplicate fields from different sources that are otherwise overwritten when merged into a single entry.

  The JSON file will have the following structure:

  ```json
  [
    {
      "entry": "<entry_id>",
      "new-fields": 8,
      "crossref": {
        "query-url": "https://api.crossref.org/...",
        "query-response-time": 0.556,
        "query-response-status": 200,
        "author" : "Lastname, Firstnames and Lastname, Firstnames ...",
        "title" : "super interesting article!",
        "..." : "..."
      },
      "arxiv": null, // null when no match found
      "dblp": ...,
      "researchr": ...,
      "unpaywall": ...
    },
    ...
  ]
  ```

- `-O --no-output` don't write any output files (except the one specified by `--dump-data`)
  can be used with `-v/--verbose` mode to only print a list of changes to the terminal

- `-v --verbose` verbose mode shows more info. It details entries as they are
  being processed and shows a summary of new fields and their source at the end.
  Using it more than once prints debug info (up to four times).
- `-s --silent` hide info and progress bar. Keep showing warnings and errors.
  Use twice to also hide warnings, thrice to also hide errors and four times to
  also hide critical errors, effectively killing all output.
- `-n --no-color` don't use ANSI codes to color and stylize output

- `--version` show version number
- `-h --help` show help
