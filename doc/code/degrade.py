"""degrade.py - A tool to apply Data Degradation to the AOL data set.

Usage: python degrade.py file

where file is the name of the AOL data file.
"""


import sys


def main(file_name):
    with open(file_name) as file:
        pass
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('Not enough arguments.\n' + __doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
