# %%
from thetadata import ThetaClient
import pandas as pd
import requests


class OptionsData(object):
    def __init__(self, username, password):
        """Wrapper for ThetaData client to obtain live options quotes

        Args:
            username (str): ThetaData username
            password (str): ThetaData password
        """
        self.client = ThetaClient(username=username, passwd=password)

    def get_expirations(self, symbol):
        with self.client.connect():
            return self.client.get_expirations(symbol)

    def get_front_silo(self, symbol, dte=False):
        today = pd.to_datetime(pd.Timestamp.today().date())
        silos = self.get_expirations(symbol)
        expiration = min(silos[silos >= today])
        if dte:
            return (expiration - today).days
        return expiration

    def get_snapshot(self, symbol, expiration=None):
        with self.client.connect():
            if expiration is None:  # Use front silo if not specified
                expiration = self.get_front_silo(symbol)
            api_url = f"http://127.0.0.1:25510/bulk_snapshot/option/quote?root={symbol}&exp={expiration.strftime('%Y%m%d')}"
            entries = []
            response = requests.get(api_url)
            for tick in response.json()['response']:
                strike = tick['contract']['strike']
                itype = tick['contract']['right']
                _, bidsize, _, bid, _, asksize, _, ask, _, _ = tick['tick']
                mprice = (bidsize*ask+asksize*bid) / \
                    (bidsize+asksize) if (bidsize+asksize) > 0 else 0
                entries.append({'Strike': strike/1000, 'Spread': round(ask -
                               bid, 2), 'MPrice': round(mprice, 2), 'IType': itype})
        return pd.DataFrame(entries).drop_duplicates()
