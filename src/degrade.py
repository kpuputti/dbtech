"""degrade.py - A tool to apply Data Degradation to the AOL data set.

Usage: python degrade.py file

where file is the name of the AOL data file.
"""
from datetime import datetime
import math
import sys


# Smoothing technique.
s = 18
# Weights.
w = [1, 0.3, 0.2, 0.1]
# Risk factors.
r = [1, 0.2, 0.1, 0.05]
# Datum intervals.
d = [0, 16, 46, 96, 96]
# Degradation steps.
n = 4
# Number of items in store.
N = 100
# Constant c.
c = 1


def wt(a, i):
    return w[i] * (1 + math.cos((a * math.pi) / 180))


def risk(datum):
    sum = 0
    for l in xrange(n):
        sum += r[l] * (d[l + 1] - d[l])
    return c * sum


def priv(datum):
    return 1 / (s + risk(datum))


def CI(datum):
    return totworth(datum) * priv(datum)


def totworth(datum):
    tsum = 0
    for l in xrange(n - 1):
        inner_sum = 0
        a = d[l]
        while a < d[l + 1]:
            inner_sum += wt(a, l)
            a += 1
        tsum += inner_sum
    return c * tsum


def degrade(datum):
    return datum


def main(file_name):
    with open(file_name) as file:
        for line in file:
            # Skip the first line with column names.
            if line.startswith('AnonID'):
                print line.rstrip()
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
            degraded = degrade(datum)
            # Print out the degraded datum.
            print '%d\t%s\t%s\t%s\t%s' % (degraded['anon_id'],
                                          degraded['query'],
                                          str(degraded['query_time']),
                                          degraded['item_rank'] or '',
                                          degraded['click_url'] or '')
    return 0


if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     sys.stderr.write('Not enough arguments.\n' + __doc__)
    #     sys.exit(2)
    # sys.exit(main(sys.argv[1]))

    print 'CI(d):', CI(d)
    print 'totworth(d):', totworth(d)
    print 'priv(d):', priv(d)
    print 'risk(d):', risk(d)
