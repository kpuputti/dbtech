"""degrade.py - A tool to apply Data Degradation to the AOL data set.

Usage: python degrade.py file

where file is the name of the AOL data file.
"""


from datetime import datetime
import sys


def totworth(datum):
    pass


def risk(datum):
    pass


def priv(datum):
    pass


def main(file_name):
    with open(file_name) as file:
        for line in file:
            # Skip the first line with column names.
            if line.startswith('AnonID'):
                continue
            # Construct the datum from the columns.
            anon_id, query, query_time, item_rank, click_url = line.split('\t')
            datum = {
                'anon_id': int(anon_id),
                'query': query,
                'query_time': datetime.strptime(query_time,
                                                '%Y-%m-%d %H:%M:%S'),
                'item_rank': item_rank or None,
                'click_url': click_url.rstrip() or None,
            }
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('Not enough arguments.\n' + __doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
