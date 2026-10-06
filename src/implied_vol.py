import numpy as np
from scipy.optimize import brentq

from src.bs_model import black_scholes_call


def implied_volatility(
        market_price,
        S,
        K,
        T,
        r,
        q=0.0
):
    """
    Solve implied volatility for a European call option
    using the Black-Scholes model and Brent's method.

    Returns np.nan if no valid solution exists.
    """


    values = (
        market_price,
        S,
        K,
        T,
        r,
        q
    )


    if not all(
        np.isfinite(x)
        for x in values
    ):
        return np.nan


    if (
        market_price < 0
        or S <= 0
        or K <= 0
        or T <= 0
    ):
        return np.nan



    lower = max(
        S*np.exp(-q*T)
        -
        K*np.exp(-r*T),
        0.0
    )


    upper = (
        S*np.exp(-q*T)
    )


    tolerance = (
        1e-10
        *
        max(1.0, upper)
    )


    if (
        market_price < lower - tolerance
        or market_price >= upper
    ):
        return np.nan


    if abs(
        market_price-lower
    ) <= tolerance:
        return 0.0



    def objective(sigma):

        return (
            black_scholes_call(
                S,
                K,
                T,
                r,
                sigma,
                q
            )
            -
            market_price
        )



    sigma_max = 5.0


    if objective(sigma_max) < 0:
        return np.nan



    return float(
        brentq(
            objective,
            0.0,
            sigma_max
        )
    )