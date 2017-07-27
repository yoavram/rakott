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


