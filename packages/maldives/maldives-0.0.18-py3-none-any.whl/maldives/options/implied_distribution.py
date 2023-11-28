import pandas as pd
import numpy as np
from derivative import dxdt


def _implied_dist(strikes, prices):
    d1 = dxdt(prices, strikes, kind="kalman", alpha=1000)
    d2 = dxdt(d1, strikes, kind="kalman", alpha=1000)

    # zero out the tails
    dist = pd.Series(d2, index=strikes)
    atm = dist.idxmax()
    otm = dist[atm:]
    itm = dist[:atm]
    max_strike, min_strike = otm.where(
        otm <= 0).first_valid_index(), itm.where(itm <= 0).last_valid_index()
    res = dist[min_strike:max_strike].iloc[1:-1]

    return res / np.trapz(res, x=res.index)


def _expectation(dist):
    return np.trapz(dist*dist.index, x=dist.index)


class OptionsImpliedPrice(object):
    def __init__(self, options_data, interest_rate):
        self.data = options_data
        self.interest_rate = interest_rate
        self.ert = {}

    def __getitem__(self, symbol):
        df = self.data.get_snapshot(symbol)
        calls = df.query('IType=="C"').sort_values('Strike')
        puts = df.query('IType=="P"').sort_values('Strike')
        if symbol not in self.ert:
            self.ert[symbol] = np.exp(-self.interest_rate *
                                      self.data.get_front_silo(symbol, dte=True)/256)
        call_implied = _expectation(_implied_dist(
            calls.Strike.values, calls.MPrice.values))*self.ert[symbol]
        put_implied = _expectation(_implied_dist(
            puts.Strike.values, puts.MPrice.values))*self.ert[symbol]
        return sorted([call_implied.round(2), put_implied.round(2)])
