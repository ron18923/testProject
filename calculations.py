# Here are all the calculation functions

import math
import numpy as np
import pandas as pd


def manual_similarity_measure(first, second):

    numerator = 0
    max_value = max(first.nlargest(1).get(0), second.nlargest(1).get(0))

    denominator = min(len(first), len(second))

    for index in range(denominator):
        numerator += (first[index]/max_value-second[index]/max_value)**2
    return 1 - math.sqrt(numerator/denominator)
