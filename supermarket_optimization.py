# This script identifies association rules based on existing records of
# buyer’s transactions at a supermarket. The input is a whitespace
# delimited data file, where each row records the SKU numbers of items
# in a single transaction. The script finds the most common items sold
# together. The set size for the common items is defined in the variable
# item_set_size, and a parameter 'sigma' defines the minimum number of
# occurances of each set to return. Default values are 3 for item_set_size
# and 4 for sigma.


import csv
import sys
from itertools import combinations
from collections import Counter


# model parameters
try:
    filename = sys.argv[1]
except IndexError:
    filename = 'retail_25k.dat'

try:
    item_set_size = int(sys.argv[2])
except IndexError:
    item_set_size = 3

try:
    sigma = int(sys.argv[3])
except IndexError:
    sigma = 4


def main():
    # Run through the data pipeline
    print('Opening file...')
    with open(filename, 'r') as f:
        data = [line.rstrip().split() for line in f]

    print('Finding all sets...  ')
    sets = find_combos(data, item_set_size)

    print('Counting all unique combinations...')
    counter = count_combos(sets)

    print('Formatting output...')
    output = format_output(counter, item_set_size, sigma)

    print('Saving file...')
    with open("output.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(output)
    print('Complete')


def find_combos(data, item_set_size=3):
    '''
    Takes a list-of-lists and a set size parameter; for each sublist finds all
    combinations of elements of length item_set_size, and returns a list of
    the lists of combinations.

    Input: [[1, 2, 3], [1, 2, 4]], 2
    Output: [[(1, 2), (1, 3), (2, 3)], [(1, 2), (2, 4), (1, 4)]]
    '''
    sets = []
    for line in data:
        sets.append(list(set(combinations(line, item_set_size))))
    return sets


def count_combos(sets):
    '''
    Takes a list-of-lists of combination sets, flattens the lists, and
    returns a list of tuples of all combinations and frequencies,
    sorted in order of frequency.

    Input: [[(1, 2), (1, 3), (2, 3)], [(1, 2), (2, 4), (1, 4)]]
    Output: [((1, 2), 2), ((1, 3), 1), ((2, 3), 1), ((2, 4), 1), ((1, 4), 1)]
    '''
    flattened = [elem for sublist in sets for elem in sublist]
    return Counter(flattened).most_common()


def format_output(counter, item_set_size, sigma):
    '''
    Takes a flattened list of tuples of combinations and frequencies,
    the item_set_size (corresponding to the length of the combinations),
    and a sigma parameter defining the minimum frequency to return.
    Adds a header row and formats the data into a list-of-lists where each
    row takes the form:
        <item set size (N)>, <co-occurrence frequency>,
        <item 1 id >, <item 2 id>, …. <item N id>

    Input: [((1, 2), 2), ((1, 3), 1), ((2, 3), 1), ((2, 4), 1), ((1, 4), 1)],
           3,
           1
    Output (excluding header): [[3, 2, 1, 2],
                                [3, 1, 1, 3],
                                [3, 1, 2, 3],
                                [3, 1, 2, 4],
                                [3, 1, 1, 4]]
    '''
    # define header
    output = [['item set size (N)', 'co-occurrence frequency']]
    output[0].extend(['item {} id'.format(N + 1)
                      for N in range(item_set_size)])
    # format and append each row
    for item_set in counter:
        if item_set[1] >= sigma:
            row = [item_set_size, item_set[1]]
            row.extend(item_set[0])
            output.append(row)
        else:
            # function takes sorted input so we can stop once sigma is reached
            return output
    return output


if __name__ == "__main__":
    main()
