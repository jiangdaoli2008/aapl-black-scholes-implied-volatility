import numpy as np
from scipy.stats import norm


def black_scholes_call(
        S,
        K,
        T,
        r,
        sigma,
        q=0.0
):
    """
    Black-Scholes European call option pricing model.

    Parameters
    ----------
    S : float
        Underlying price

    K : float
        Strike price

    T : float
        Time to maturity (years)

    r : float
        Continuous risk-free rate

    sigma : float
        Volatility

    q : float
        Continuous dividend yield

    Returns
    -------
    float
        Call option price
    """


    S = float(S)
    K = float(K)
    T = float(T)
    r = float(r)
    sigma = float(sigma)
    q = float(q)


    values = (
        S,
        K,
        T,
        r,
        sigma,
        q
    )


    if not all(
        np.isfinite(x)
        for x in values
    ):
        raise ValueError(
            "Inputs must be finite numbers"
        )


    if S <= 0 or K <= 0:
        raise ValueError(
            "S and K must be positive"
        )


    if T < 0 or sigma < 0:
        raise ValueError(
            "T and sigma must be non-negative"
        )


    if T == 0:
        return max(S-K,0.0)


    if sigma == 0:
        return max(
            S*np.exp(-q*T)
            -
            K*np.exp(-r*T),
            0.0
        )


    sqrt_T = np.sqrt(T)


    d1 = (
        np.log(S/K)
        +
        (r-q+0.5*sigma**2)*T
    ) / (
        sigma*sqrt_T
    )


    d2 = (
        d1
        -
        sigma*sqrt_T
    )


    price = (
        S*np.exp(-q*T)*norm.cdf(d1)
        -
        K*np.exp(-r*T)*norm.cdf(d2)
    )


    return float(price)