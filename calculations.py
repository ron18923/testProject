# Here are all the calculation functions

import math
import numpy as np


def manual_similarity_measure(first, second):

    numerator = 0
    max_value = np.maximum(first, second)

    shorter = max(first, second)
    denominator = len(shorter)

    for index in range(shorter):
        numerator += (arg[0]/max_value-arg[1]/max_value)**2

    return 1 - math.sqrt(numerator/denominator)
