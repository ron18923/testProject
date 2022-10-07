# Here are all the calculation functions

import math


def manual_similarity_measure(first, second):
    numerator = 0

    min_first = first.nsmallest(1).get(0)
    min_second = second.nsmallest(1).get(0)

    for index in range(len(first)):
        first[index] = first[index] - min_first

    for index in range(len(second)):
        second[index] = second[index] - min_second

    max_value = max(first.nlargest(1).get(0), second.nlargest(1).get(0))

    denominator = min(len(first), len(second))

    for index in range(denominator):
        numerator += (first[index] / max_value - second[index] / max_value) ** 2
    return 1 - math.sqrt(numerator / denominator)
