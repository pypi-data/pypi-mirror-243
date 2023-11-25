from fredapi import Fred


class FredData(object):
    def __init__(self, api_key):
        """Class containing named shortcuts to useful FRED series.

        Args:
            api_key (string): FRED API key
        """
        self.client = Fred(api_key)

    def _get_series(series, name): return (lambda self, start=None,
                                           end=None: self.client.get_series(series, start, end).rename(name))

    CPI = _get_series('CPIAUCSL', 'CPI')
    Treasury10Y = _get_series('DGS10', 'Treasury10Y')
    InterestRate = _get_series('AMERIBOR', 'InterestRate')
