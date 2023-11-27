from numpy import log, sqrt
import numpy as np
import sys

# These routines have been copied from PyOTE  5.4.8

# This routine was a 'generator' in PyOTE, but have been converted to a normal procedure here.
# We also eliminated the test for and solution found being better than a straight line as that would
# be always true.
def find_best_r_only_from_min_max_size(
        y: np.ndarray, left: int, right: int, min_event: int, max_event: int):
    """Finds the best r-only location for r >=  min_event and <=  max_event"""

    assert min_event >= 1
    assert max_event <= right - left

    def update_best_solution():
        nonlocal max_metric, b_best, a_best, sigma_b, sigma_a
        nonlocal r_best

        max_metric = metric
        b_best = b
        a_best = a
        sigma_b = sqrt(b_var)
        sigma_a = sqrt(a_var)
        r_best = r

    def calc_metric():
        nonlocal a_var, b_var
        max_var = max(a_var, b_var, sys.float_info.min)

        if a_var <= 0.0:
            a_var = max_var
        if b_var <= 0.0:
            b_var = max_var
        return -b_n * log(b_var) - a_n * log(a_var)

    # These get changed by the first call to update_best_solution but
    # have the be set to proper type to satisfy type checking.
    metric = 0.0
    max_metric = 0.0
    r_best = 0
    b_best = 0.0
    a_best = 0.0
    sigma_b = 0.0
    sigma_a = 0.0

    r = left + min_event

    # Use numpy version of metric calculator to initialize iteration variables

    # B excludes y[r] and the extra point at right - but this is meaningless because r is incorrect at this point
    b_s, b_s2, b_n, b_var = calc_metric_numpy(y[r + 1:right])

    # A always excludes y[r]) - but this is meaningless because r is incorrect at this point
    a_s, a_s2, a_n, a_var = calc_metric_numpy(y[left + 1:r])

    b = b_s / b_n
    a = a_s / a_n

    # Calculate metric for initial position of r
    metric = calc_metric()
    update_best_solution()

    r_final = left + max_event - 1

    while r < r_final:
        # calc metric for next r position from current position

        a_s, a_s2, a_n, a_var = add_entry(y[r], a_s, a_s2, a_n, True)
        r += 1
        b_s, b_s2, b_n, b_var = sub_entry(y[r], b_s, b_s2, b_n, True)


        metric = calc_metric()
        b = b_s / b_n
        a = a_s / a_n

        # goodSolution = solution_is_better_than_straight_line(
        #         y, left, right, -1, r, b, a, sqrt(b_var), sqrt(a_var), k=3)
        goodSolution = True

        if metric > max_metric and b > a and goodSolution:
            update_best_solution()

    if b_best <= a_best:
        # yield 'no event present', 1.0
        return 'no event found', -1, -1, 0.0, 0.0, 0.0, 0.0, 0.0

    event_size_found = r_best - left
    if event_size_found == max_event or event_size_found == min_event:
        # Invalid event size --- invalid limit
        return 'invalid event size', -1, -1, 0.0, 0.0, 0.0, 0.0, 0.0

    # Here we test for the best solution being better than straight line
    # if not solution_is_better_than_straight_line(
    #         y, left, right, -1, r_best, b, a, sigma_b, sigma_a, k=3):
    #     # yield 'no event present', 1.0
    #     yield -1.0, 1.0, -1, -1, 0.0, 0.0, 0.0, 0.0, 0.0

    return 'ok', -1, r_best, b_best, a_best, sigma_b, sigma_a, max_metric


def calc_metric_numpy(y: np.ndarray):
    """Used for timing comparisons and initializing a metric from a large y[].

    It calculates the metrics using fast numpy operations.
    """

    n = y.size
    s2 = np.sum(y * y)
    s = y.sum()
    var = (s2 - s * s / n) / n  # This is sigma**2

    return s, s2, n, var

def add_entry(ynew: float, s: float, s2: float, n: int, calc_var: bool):
    """Adds an entry to the metrics, s, s2, and n.

    s:  previous value of sum of y[]
    s2: previous value of sum of y[]*y[]
    n:  previous number of entries in the metric
    """

    n = n + 1
    s = s + ynew
    s2 = s2 + ynew * ynew

    if calc_var:
        var = (s2 - s * s / n) / n  # This is sigma**2
    else:
        var = None

    return s, s2, n, var

def sub_entry(ynew: float, s: float, s2: float, n: int, calc_var: bool):
    """Subtracts an entry from the metrics, s, s2, and n.

    s:  previous value of sum of y[]
    s2: previous value of sum of y[]*y[]
    n:  previous number of entries in the metric
    """

    n = n - 1
    s = s - ynew
    s2 = s2 - ynew * ynew

    if calc_var:
        var = (s2 - s * s / n) / n  # This is sigma**2
    else:
        var = None

    return s, s2, n, var

def subFrameAdjusted(*, eventType='Ronly', cand=None, B=None, A=None,
                     sigmaA=None, sigmaB=None,
                     yValues=None, left=None, right=None):

    def adjustR():
        value = yValues[R]
        adj = (B - value) / (B - A)
        return R + adj

    def adjustD():
        value = yValues[D]
        adj = (value - A) / (B - A)
        return D + adj

    transitionPoints = []

    D, R = cand
    adjD = D
    adjR = R

    # Here we add code so we can analyze light curves that may have sigmaB or
    #  sigmaA values of zero.  This happens when testing with artificial data
    #  but can also result from real light curves that may be clipped so that
    #  all B pixels have a constant value.  Limovie can produce a sigmaA=0
    # when a rectangular aperture is in use as well

    if eventType == 'Donly':
        if aicModelValue(obsValue=yValues[D], B=B, A=A, sigmaB=sigmaB, sigmaA=sigmaA) == yValues[D]:
            # If point at D categorizes as M (valid mid-point), do sub-frame
            # adjustment and exit
            adjD = adjustD()
            transitionPoints.append(D)
            B, A, sigmaB, sigmaA = newCalcBandA(yValues=yValues, tpList=transitionPoints,
                                                left=left, right=right, cand=(D, R))
        elif aicModelValue(obsValue=yValues[D], B=B, A=A, sigmaB=sigmaB, sigmaA=sigmaA) == B:
            # else if point at D categorizes as B, set D to D+1 and recalculate B and A
            D = D + 1
            adjD = D
            B, A, sigmaB, sigmaA = newCalcBandA(yValues=yValues, tpList=transitionPoints,
                                                left=left, right=right, cand=(D, R))
            # It's possible that this new point qualifies as M --- so we check:
            if aicModelValue(
                    obsValue=yValues[D], B=B, A=A, sigmaB=sigmaB,
                    sigmaA=sigmaA) == yValues[D]:
                adjD = adjustD()
                transitionPoints.append(D)
                B, A, sigmaB, sigmaA = newCalcBandA(yValues=yValues, tpList=transitionPoints,
                                                    left=left, right=right, cand=(D, R))
        # else (point at D categorizes as A) --- nothing to do
        return [adjD, adjR], B, A, sigmaB, sigmaA

    elif eventType == 'Ronly':
        if aicModelValue(obsValue=yValues[R], B=B, A=A, sigmaB=sigmaB, sigmaA=sigmaA) == yValues[R]:
            # If point at R categorizes as M, do sub-frame adjustment
            adjR = adjustR()
            transitionPoints.append(R)
            B, A, sigmaB, sigmaA = newCalcBandA(yValues=yValues, tpList=transitionPoints,
                                                left=left, right=right, cand=(D, R))
        elif aicModelValue(obsValue=yValues[R], B=B, A=A, sigmaB=sigmaB, sigmaA=sigmaA) == A:
            # else if point at R categorizes as A, set R to R + 1 and recalculate B and A
            R = R + 1
            adjR = R
            B, A, sigmaB, sigmaA = newCalcBandA(yValues=yValues, tpList=transitionPoints,
                                                left=left, right=right, cand=(D, R))
            # It's possible that this new point qualifies as M --- so we check
            if aicModelValue(
                    obsValue=yValues[R], B=B, A=A, sigmaB=sigmaB,
                    sigmaA=sigmaA) == yValues[R]:
                adjR = adjustR()
                transitionPoints.append(R)
                B, A, sigmaB, sigmaA = newCalcBandA(yValues=yValues, tpList=transitionPoints,
                                                    left=left, right=right, cand=(D, R))
        elif aicModelValue(obsValue=yValues[R - 1], B=B, A=A, sigmaB=sigmaB,
                           sigmaA=sigmaA) == yValues[R - 1]:
            # The point at R categorizes as B, and we have found
            # that the point at R-1 categorizes as M, so set R to R-1 and
            # recalculate B and A
            R = R - 1
            adjR = adjustR()
            transitionPoints.append(R)
            B, A, sigmaB, sigmaA = newCalcBandA(yValues=yValues, tpList=transitionPoints,
                                                left=left, right=right, cand=(D, R))
        return [adjD, adjR], B, A, sigmaB, sigmaA

    elif eventType == 'DandR':
        if not R - D > 2:
            return [D, R], B, A, sigmaB, sigmaA
        if aicModelValue(
                obsValue=yValues[D], B=B, A=A, sigmaB=sigmaB, sigmaA=sigmaA) == yValues[D]:
            # The point at D categorizes as M, do sub-frame adjustment; this
            # (finishes D)
            adjD = adjustD()
            transitionPoints.append(D)
        elif aicModelValue(obsValue=yValues[D], B=B, A=A, sigmaB=sigmaB, sigmaA=sigmaA) == B:
            # The point at D categorizes as B, set D to D+1 and recalculate B and A
            D = D + 1
            adjD = D
            # It's possible that this new point qualifies as M --- so we check
            if aicModelValue(
                    obsValue=yValues[D], B=B, A=A, sigmaB=sigmaB,
                    sigmaA=sigmaA) == yValues[D]:
                adjD = adjustD()
                transitionPoints.append(D)
        elif aicModelValue(obsValue=yValues[D-1], B=B, A=A, sigmaB=sigmaB,
                           sigmaA=sigmaA) == yValues[D-1]:
            # The point at D categorizes as A, and we have found
            # that the point at D-1 categorizes as M, so set D to D-1 and
            # recalculate B and A
            D = D - 1
            adjD = adjustD()
            transitionPoints.append(D)

        if aicModelValue(
                obsValue=yValues[R], B=B, A=A, sigmaB=sigmaB, sigmaA=sigmaA) == yValues[R]:
            # The point at R categorizes as M, do sub-frame adjustment
            adjR = adjustR()
            transitionPoints.append(R)
        elif aicModelValue(obsValue=yValues[R], B=B, A=A, sigmaB=sigmaB, sigmaA=sigmaA) == A:
            # The point at R categorizes as A, set R to R + 1 and recalculate B and A
            R = R + 1
            adjR = R
            # It's possible that this new point qualifies as M --- so we check
            if aicModelValue(
                    obsValue=yValues[R], B=B, A=A, sigmaB=sigmaB,
                    sigmaA=sigmaA) == yValues[R]:
                adjR = adjustR()
                transitionPoints.append(R)
        elif aicModelValue(obsValue=yValues[R - 1], B=B, A=A, sigmaB=sigmaB,
                           sigmaA=sigmaA) == yValues[R - 1]:
            # The point at R categorizes as B, and we have found
            # that the point at R-1 categorizes as M, so set R to R-1 and
            # recalculate B and A
            R = R - 1
            adjR = adjustR()
            transitionPoints.append(R)
        return [adjD, adjR], B, A, sigmaB, sigmaA

    else:
        raise Exception('Unrecognized event type')

def aicModelValue(*, obsValue=None, B=None, A=None, sigmaB=None, sigmaA=None):
    assert B >= A
    # assert sigmaA > 0.0
    # assert sigmaB > 0.0

    # This function determines if an observation point should categorized as a baseline (B)
    # point, an event (A) point, or a valid intermediate point using the Akaike Information Criterion
    # An intermediate point reflects a more complex model (higher dimension model)
    if obsValue >= B:
        return B  # Categorize as baseline point
    if obsValue <= A:
        return A  # Categorize as event point
    if B == A:
        return B

    # We do this to allow test files with zero noise to be processed
    if sigmaA == 0:
        if sigmaB == 0:
            return obsValue
        else:
            assert sigmaA > 0.0

    sigmaM = sigmaA + (sigmaB - sigmaA) * ((obsValue - A) / (B - A))
    loglB = loglikelihood(obsValue, B, sigmaB)
    loglM = loglikelihood(B, B, sigmaM) - 1.0  # The -1 is the aic model complexity 'penalty'
    loglA = loglikelihood(obsValue, A, sigmaA)

    if loglM > loglA and loglM > loglB:
        return obsValue  # Categorize as valid intermediate value
    elif loglB > loglA:
        return B  # Categorize as baseline point
    else:
        return A  # Categorize as event point

def loglikelihood(y, m, sigma):
    """ calculate ln(likelihood) given Gaussian statistics

    Args:
        y (float):     measured value
        m (float):     mean (expected model value)
        sigma (float): stdev of measurements

    Returns:
        natural logarithm of un-normalized probability based on Gaussian distribution

    """
    # log(x) is natural log (base e)
    # -log(sqrt(2*pi)) = -0.9189385332046727
    # t1 = -log(sqrt(2*pi))
    t1 = -0.9189385332046727
    t2 = -log(sigma)
    t3 = -(y - m) ** 2 / (2 * sigma ** 2)
    return t1 + t2 + t3

def newCalcBandA(*, yValues=None, tpList=None, left=None, right=None, cand=None):
    assert (right > left)

    sigmaA = 0.0

    def valuesToBeUsed(lowRange, highRange):
        valList = []
        for i in range(lowRange, highRange):
            if i not in tpList:
                valList.append(yValues[i])
        return valList

    D, R = cand  # Extract D and R from the tuple

    if R is None:
        assert (D >= left)
        # This is a 'Donly' candidate
        # Note that the yValue at D is not included in the B calculation
        # because that point is in the event bottom.
        valuesToUse = valuesToBeUsed(left, D)
        B = np.mean(valuesToUse)
        sigmaB = np.std(valuesToUse)
        # We have to deal with a D at the right edge.  There is no value to
        # the right to use to calculate A so we simply return the value at D
        # as the best estimate of A
        if D == right:
            A = yValues[D]
            sigmaA = 0.0
        else:
            # changed in 4.4.7
            # A = np.mean(yValues[D+1:right+1])
            valuesToUse = valuesToBeUsed(D, right + 1)
            A = np.mean(valuesToUse)
            sigmaA = np.std(valuesToUse)
        if A >= B:
            A = B * 0.999
        return B, A, sigmaB, sigmaA

    elif D is None:
        assert (R <= right)
        # This is an 'Ronly' candidate
        # We have to deal with a R at the right edge.  There is no value to
        # the right to use to calculate B so we simply return the value at R
        # as the best estimate of B
        if R == right:
            B = yValues[R]
            sigmaB = 0.0
        else:
            # changed in 4.4.7
            # B = np.mean(yValues[R+1:right+1])
            # Changed i to i + R in 5.2.3 to solve flash edge time problem
            valuesToUse = [val for i, val in enumerate(yValues[R:right + 1]) if i + R not in tpList]
            B = np.mean(valuesToUse)
            sigmaB = np.std(valuesToUse)
        # Changed to R - 1 in 5.2.3 to solve flash edge time problem
        valuesToUse = valuesToBeUsed(left, R - 1)
        A = np.mean(valuesToUse)
        sigmaA = np.std(valuesToUse)
        if A >= B:
            A = B * 0.999
        return B, A, sigmaB, sigmaA

    else:
        assert ((D >= left) and (R <= right) and (R > D))
        # We have a 'DandR' candidate
        leftBvals = valuesToBeUsed(left, D)

        if R == right:
            rightBvals = yValues[right]
        else:
            # changed in 4.4.8
            rightBvals = valuesToBeUsed(R, right + 1)
        B = (np.sum(leftBvals) + np.sum(rightBvals)) / (len(leftBvals) + len(rightBvals))
        sigmaB = np.std(leftBvals + rightBvals)

        if R - D == 1:  # Event size of 1 has no valid A --- we choose the value at D
            A = yValues[D]
        else:
            valuesToUse = valuesToBeUsed(D, R)
            A = np.mean(valuesToUse)
            sigmaA = np.std(valuesToUse)
        if A >= B:
            A = B * 0.999
        return B, A, sigmaB, sigmaA
