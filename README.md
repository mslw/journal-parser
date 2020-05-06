# journal-parser
Perform fuzzy search on Ministry list of journals

## Introduction
The Ministry of Science and Education list of journals, containing scoring and discipline classification, is published
in an unwieldy 6.5 MB excel file. I wrote this simple script to reduce the opening time (by using feather format) and allow
searching without having to be single-letter accurate with journal titles (by using fuzzywuzzy library).

## Usage
### Preparation: loading the database (required only once)
1) Download the official xlsx file from the Ministry webpage (The 2019 version can be found [here](http://www.bip.nauka.gov.pl/akty-prawne-mnisw/komunikat-ministra-nauki-i-szkolnictwa-wyzszego-z-dnia-31-lipca-2019-r-w-sprawie-wykazu-czasopism-naukowych-i-recenzowanych-materialow-z-konferencji-miedzynarodowych-wraz-z-przypisana-liczba-punktow.html)).
2) Run the following to convert the excel file into feather format (this dramatically speeds up loading with pandas):
`python search.py --prepare-db path/to/the/list.xlsx`

### Searching
To search, type: `python search.py "Title of the journal"`.

Please note that if the title contains multiple words, it needs to be placed in quotes (to be treated as single argument).
The search will take a few seconds and the closest match will be reported.

### Example usage & output
```
$ python search.py "Frontiers of Neuroscience"
ISSN 1662-453X
eISSN 1662-453X
Tytuł 1: Frontiers in Neuroscience
Tytuł 2: Frontiers in Neuroscience
Punkty: 100
Nauki biologiczne: TAK
```

## Requirements
Requires Python 3 with the following libraries:
* pandas
* pyarrow
* xlrd
* fuzzywuzzy
* python-Levenshtein

The requirements file with specific versions used during development is provided (but the versions aren't crucial).

## Limitations
1) The script relies on several features of the 2019 table formatting (e.g. it assumes that biological sciences column
is labelled with 604). If the formatting changes notably for future Ministry releases, it may crash or produce wrong output.
2) The search is performed only on the first title column.
2) Always returns only one match.

## Contributing
Contributions adding new functionality or mitigating the limitations listed above are welcome.
