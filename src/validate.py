from datetime import datetime
import math


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


if __name__ == '__main__':
    print 'CI(d):', CI(d)
    print 'totworth(d):', totworth(d)
    print 'priv(d):', priv(d)
    print 'risk(d):', risk(d)
