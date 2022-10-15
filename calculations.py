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


def manual_similarity_measure2(first, second, upscale=True):
    """
    second function(second try) to calculate similarity of line graphs accurately. The LOWEST returned value should be
    the most similar!(returns value ranging from 0 to ∞)
    :param upscale: upscaling first graph values to the second graph values by the first value of each value's list.
    Default value is True.
    :param first: first list of graph values
    :param second: second list of graph values
    :return: returns the average distance of the graphs from each other. The most similar should be with the LOWEST
    value!(returns value ranging from 0 to ∞)
    """
    subtract_amount = first[0] - second[0]

    if upscale:
        # first_first = first[0]
        # first_second = second[0]
        #
        # upscale_by = first_second / first_first
        #
        # for index in range(len(first)):
        #     first[index] *= upscale_by

        # ---not working---
        pass

    for index in range(len(first)):
        first[index] -= subtract_amount

    distances_sum = 0
    for index in range(len(first)):
        distances_sum += abs(first[index] - second[index])

    average_distance = distances_sum / len(first)
    return average_distance


def moving_average(data, length, ma_size):
    cut_data = data["close"]
    cut_data = cut_data[len(data) - length - ma_size: len(data) - length]

    total_close_sum = 0
    for index in range(len(cut_data)):
        total_close_sum += float(cut_data[index])

    average = total_close_sum / len(cut_data)
    if float(cut_data[len(cut_data) - 1]) > average:
        return average, True
    else:
        return average, False
