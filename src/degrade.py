from datetime import datetime
from matplotlib import pyplot as plt
import math
import operator
import sys


# Path to the file that hold the data.
DATA_FILE = 'data/user.txt'


# Value to apply to calculations to escape mathematical problems and
# to provide a more realistic model of privacy.
SMOOTHING_FACTOR = 18


def get_data():
    """Read and parse the input data."""
    data = []
    with open(DATA_FILE) as f:
        for line in f:
            columns = line.decode('utf-8').split('\t')
            anon_id = int(columns[0])
            query = columns[1]
            timestamp = datetime.strptime(columns[2], '%Y-%m-%d %H:%M:%S')
            item_rank = int(columns[3]) if columns[3] else None
            click_url = columns[4].rstrip() or None
            data.append((anon_id, query, timestamp, item_rank, click_url))
    return data


def weight(age):
    """The weight factor for the given age."""
    days = age.days
    if days < 21:
        # Under 3 weeks old.
        return 1
    elif days < 42:
        # 3 to 6 weeks old.
        return 0.3
    elif days < 63:
        # 6 to 9 weeks old.
        return 0.2
    else:
        # Over 9 weeks old.
        return 0.1


def wt(age):
    """Worth of one datum to the service provider."""
    return weight(age) * (1 + math.cos((age.days * math.pi) / 180))


def totworth(data, timestamp):
    """Total worth of the data to the service provider."""
    return sum(wt(timestamp - datum[2]) for datum in data)


def risk(data):
    """Risk factor of the data for the user."""
    return len(data)


def priv(data):
    """Privacy guarantee of the data to the user."""
    return 1 / (SMOOTHING_FACTOR * risk(data))


def CI(data, timestamp):
    """Common interest count for the data."""
    return totworth(data, timestamp) * priv(data, SMOOTHING_FACTOR)


def print_stats(data, timestamp, degradation_steps, risk_factor):
    print 'Degradation steps:', degradation_steps
    print 'risk factor:', risk_factor
    print 'total worth:', totworth(data, timestamp)
    print ''


def graph(values, title, xlabel, ylabel, file_name):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([x for x, y in values], [y for x, y in values], 'o-')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.savefig('output/%s' % file_name)


def generate_graphs(data, timestamp, mindate, maxdate):
    weights = []
    for datum in data:
        age = timestamp - datum[2]
        dweight = weight(age)
        weights.append((age.days, dweight))
    graph(weights, 'weights', 'age', 'weight', 'weights.png')

def main(operation):
    weights = (1, 0.3, 0.2, 0.1)
    risk_factors = (1, 0.2, 0.1, 0.05)
    intervals = (0, 16, 46, 96, 96)

    data = get_data()
    data.sort(key=operator.itemgetter(2))

    mindate = min(datum[2] for datum in data)
    maxdate = max(datum[2] for datum in data)

    # The timestamp that is considered as the current one.
    timestamp = maxdate

    # Time difference between the min and max timestamps.
    delta = maxdate - mindate

    if operation == 'stats':
        for i, (weight, risk_factor) in enumerate(zip(weights, risk_factors)):
            print_stats(data, timestamp, i, risk_factor)
    elif operation == 'graphs':
        generate_graphs(data, timestamp, mindate, maxdate)
    else:
        sys.stderr.write("Invalid argument '%s'.\n" % operation)
        return 1

    print 'datums:', len(data)
    print 'earliest timestamp:', mindate
    print 'latest timestamp:', maxdate
    print 'delta days:', delta.days

    return 0


if __name__ == '__main__':
    args = sys.argv[1:]
    n = len(args)
    if n == 1:
        sys.exit(main(args[0]))
    else:
        sys.stderr.write('Not enough arguments.\n')
