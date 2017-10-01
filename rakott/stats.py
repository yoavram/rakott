import numpy as np
import statsmodels.api as sm
import pandas as pd
import scipy.stats


def logistic_regression(X, y):
    logit = sm.Logit(y, X)
    result = logit.fit()
    summary = pd.concat([
        np.exp(result.params),
        np.exp(result.conf_int()),
        result.pvalues
    ], axis=1)
    summary.columns = ['Odds ratio', '95% CI Low', '95% CI High', 'P-value']
    return summary

def bin_prop_jeffreys_interval(trials, successes, α=0.05):
    """Binomial proportions confidence Jeffrey's interval.

    Parameters
    ----------
    trials : np.ndarray
        number of trials
    successes : int
        number of successes
    α : float, 0<α<1
        width of confidence interval

    Returns
    -------
    low, high : tuple of floats
        The lower and upper bounds of the proportions confidence interval

    See
    ---
    https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Jeffreys_interval
    """
    n = int(trials)
    x = int(successes)
    assert 0 <= x <= n
    beta = scipy.stats.beta(x + 0.5, n - x + 0.5)
    if x == 0:
        low = 0
    else:
        low = beta.ppf(α / 2)
    if x == n:
        high = 1
    else:
        high = beta.ppf(1 - α / 2)
    return x / n - low, high - x / n

def bin_prop_bs_interval(x, n, α=0.05, resamples=10000):
    """Binomial proportions confidence interval with bootstrap.

    Parameters
    ----------
    x : np.ndarray
        array of proportions
    n : int
        number of observations made when calculating proportions in `x`
    resamples : int
        number of bootstrap resamples
    α : float, 0<α<1
        width of confidence interval

    Returns
    -------
    low, high : tuple of floats
        The lower and upper bounds of the proportions confidence interval
    """
    samples = np.random.binomial(n, x, resamples)
    low = np.percentile(samples, 100*α/2)
    high = np.percentile(samples, 100*(1-α/2))
    return x-low/n, high/n-x


def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.

    Slightly modified from http://scipy.github.io/old-wiki/pages/Cookbook/SavitzkyGolay

    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
  
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
  
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.

    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()

    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    import numpy as np
    from math import factorial
    
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')
