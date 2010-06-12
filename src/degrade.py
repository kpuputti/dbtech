from datetime import datetime
import math
import sys


# Path to the file that hold the data.
DATA_FILE = 'data/user.txt'


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


def wt(weight, timedelta):
    """Worth of one datum to the service provider."""
    return weight * (1 + math.cos((timedelta.days * math.pi) / 180))


def totworth(data, timestamp, weight):
    """Total worth of the data to the service provider."""
    return sum(wt(weight, timestamp - datum[2]) for datum in data)


def risk(data):
    return len(data)


def priv(data, smoothing_factor):
    return 1 / (smoothing_factor * risk(data))


def CI(data):
    pass


def stats(data, timestamp, degradation_steps, weight, risk_factor):
    print '\nDegradation steps:', degradation_steps
    print 'weight:', weight
    print 'risk factor:', risk_factor
    print 'total worth:', totworth(data, timestamp, weight)


def main(args):
    smoothing_factor = 18
    weights = (1, 0.3, 0.2, 0.1)
    risk_factors = (1, 0.2, 0.1, 0.05)
    intervals = (0, 16, 46, 96, 96)

    data = get_data()
    min_timestamp = min(datum[2] for datum in data)
    max_timestamp = max(datum[2] for datum in data)

    # The timestamp that is considered as the current one.
    timestamp = max_timestamp

    # Time difference between the min and max timestamps.
    delta = max_timestamp - min_timestamp

    print 'datums:', len(data)
    print 'earliest timestamp:', min_timestamp
    print 'latest timestamp:', max_timestamp
    print 'delta days:', delta.days

    for i, (weight, risk_factor) in enumerate(zip(weights, risk_factors)):
        stats(data, timestamp, i, weight, risk_factor)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
