import argparse
import pandas
from fuzzywuzzy import process


def colFix(x):
    """Convert column name to string, removing dots and spaces"""
    if type(x) is int:
        return 'd{}'.format(x)
    else:
        return x.replace('.', '').replace(' ', '').replace('-', '')


def prepareTable(excel_file, feather_file):
    """Read excel table and save it to feather for faster access"""
    table = pandas.read_excel(excel_file, skiprows=3)
    table.columns = table.columns.map(colFix)
    table.to_feather(feather_file)


def findJournal(title, table):
    """Perform fuzzy search on 1st title column"""
    match = process.extractOne(title, table.Tytuł1)
    row_id = match[-1]
    match = table.loc[row_id]

    return match

def printFormatted(match):
    """Print relevant information from table row"""
    isBio = 'TAK' if match.d604 == 'x' else 'NIE'
    print('ISSN', match.issn)
    print('eISSN', match.eissn)
    print('Tytuł 1:', match.Tytuł1)
    print('Tytuł 2:', match.Tytuł2)
    print('Punkty:', match.Punkty)
    print('Nauki biologiczne:', isBio)


if __name__ == '__main__':

    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--prepare-db',
                        help='Load data from excel table')
    parser.add_argument('name', nargs='?', default=None,
                        help='Journal name')
    args = parser.parse_args()

    # constants
    DB_FILE = 'czasopisma.feather'

    # convert from excel to feather if --prepare-db specified
    if args.prepare_db is not None:
        prepareTable(args.prepare_db, DB_FILE)

    # search for journal if name specified
    if args.name is not None:
        # read the feather file
        try:
            table = pandas.read_feather(DB_FILE)
        except IOError:
            print('Cannot find {}. Run --prepare-db first'.format(DB_FILE))
            exit()

        # find and display the match
        best_match = findJournal(args.name, table)
        printFormatted(best_match)
