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


def normalize(values, scale_max=100):
    """Normalize a list of values to be within 0 and scale_max."""
    max_item = max(values)
    min_item = min(values)
    delta = float(max_item - min_item)
    return [((v - min_item) / delta) * scale_max for v in values]


def get_weight(age):
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


def get_risk_factor(age):
    """The risk factor for the given age."""
    days = age.days
    if days < 21:
        # Under 3 weeks old.
        return 1
    elif days < 42:
        # 3 to 6 weeks old.
        return 0.2
    elif days < 63:
        # 6 to 9 weeks old.
        return 0.1
    else:
        # Over 9 weeks old.
        return 0.05


def wt(age, use_weight=False):
    """Worth of one datum to the service provider."""
    weight = 1
    if use_weight:
        weight = get_weight(age)
    return weight * (1 + math.cos((age.days * math.pi) / 180))


def totworth(data, timestamp):
    """Total worth of the data to the service provider."""
    tsum = 0
    for datum in data:
        date = datum[2]
        if date < timestamp:
            delta = timestamp - date
            tsum += wt(delta)
    return tsum


def risk(data, timestamp):
    """Risk factor of the data for the user."""
    tsum = 0.0
    for datum in data:
        date = datum[2]
        if date < timestamp:
            delta = timestamp - date
            tsum += get_risk_factor(delta)
    return tsum / len(data)


def priv(data, timestamp):
    """Privacy guarantee of the data to the user."""
    return 1 / float(SMOOTHING_FACTOR + risk(data, timestamp))


def normalized_ci(retentions, tot_worths, privacies):
    """Calculate the list of common interest values."""
    ci = []
    worths = normalize(tot_worths, scale_max=100.0)
    privs = normalize(privacies, scale_max=100.0)
    for period, worth, privacy in zip(retentions, worths, privs):
        ci.append((period, worth * privacy))
    return ci


def print_stats(data, timestamp, degradation_steps, risk_factor):
    print 'Degradation steps:', degradation_steps
    print 'risk factor:', risk_factor
    print 'total worth:', totworth(data, timestamp)
    print ''


def graph(values, title, xlabel, ylabel, file_name, xticks=None):
    """Generate a graph of the provided values."""
    if xticks is None:
        xticks = (21, 42, 63, 84)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([x for x, y in values], [y for x, y in values], 'o-')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    plt.xticks(xticks)
    fig.savefig('output/%s' % file_name)


def generate_graphs(data, timestamp, mindate, maxdate):
    ages = []
    for i in xrange(100):
        ages.append([i, 0])

    weights = []
    worths = []
    worths_weighted = []
    tot_worths = []
    risks = []
    privacies = []
    common_interests = []

    for datum in data:
        date = datum[2]
        assert date <= timestamp
        age = timestamp - date
        retention_period = date - mindate

        ages[age.days][1] += 1
        weights.append((age.days, get_weight(age)))
        worths.append((age.days, wt(age, use_weight=False)))
        worths_weighted.append((age.days, wt(age, use_weight=True)))

        tot_worths.append((retention_period.days, totworth(data, date)))
        risks.append((retention_period.days, risk(data, date)))
        privacies.append((retention_period.days, priv(data, date)))

    common_interests = normalized_ci([d for d, w in tot_worths],
                                     [w for d, w in tot_worths],
                                     [p for d, p in privacies])

    graph(ages, 'number of data items per day', 'days from the first date', 'count',
          'ages.png')
    graph(weights, 'weights', 'age', 'weight', 'weights.png')
    graph(worths, 'worths', 'age', 'worth', 'worths.png')
    graph(worths_weighted, 'worths with weights', 'age', 'worth',
          'worths_weighted.png')

    graph(tot_worths, 'total worth of the db at certain point in time',
          'retention period in days', 'total worth', 'tot_worths.png')
    graph(privacies, 'privacy value at certain point in time',
          'retention period in days', 'privacy value', 'privacies.png')
    graph(risks, 'risk value at certain point in time',
          'retention period in days', 'risk value', 'risks.png')
    graph(common_interests, 'common interest value at certain point in time',
          'retention period in days', 'common interest', 'common_interests.png')


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
