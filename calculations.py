# Here are all the calculation functions

import math


def manual_similarity_measure(first, second):
    """
    first function(first try) to calculate similarity of line graphs accurately. The HIGHEST returned value should be
    the most similar! (returns value ranging from 0 to 1)
    :param first: first list of graph values
    :param second: second list of graph values
    :return: returns the average distance of the graphs from each other. The most similar should be with the HIGHEST
    value!(returns value ranging from 0 to 1)
    """
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


def manual_similarity_measure2(first, second):
    """
    second function(second try) to calculate similarity of line graphs accurately. The LOWEST returned value should be
    the most similar!(returns value ranging from 0 to ∞)
    :param first: first list of graph values
    :param second: second list of graph values
    :return: returns the average distance of the graphs from each other. The most similar should be with the LOWEST
    value!(returns value ranging from 0 to ∞)
    """
    subtract_amount = first[0]-second[0]

    for index in range(len(first)):
        first[index] -= subtract_amount

    distances_sum = 0
    for index in range(len(first)):
        distances_sum += abs(first[index] - second[index])

    average_distance = distances_sum/len(first)
    return average_distance
