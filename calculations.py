# Here are all the calculation functions

import math
import numpy as np


def manual_similarity_measure(*argv):
    # input type: [x,y]

    denominator = len(argv)

    max_value = np.amax(argv)

    numerator = 0
    for arg in argv:
        numerator += (arg[0]/max_value-arg[1]/max_value)**2

    return 1 - math.sqrt(numerator/denominator)
