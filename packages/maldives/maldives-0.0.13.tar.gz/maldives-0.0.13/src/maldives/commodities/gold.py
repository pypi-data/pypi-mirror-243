from wallstreet import Stock
from maldives.regression import LinearRegressor
from maldives.api import FredData

import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots


class GoldPriceModel(object):
    def __init__(self):
        self.df = None
        self.fitted = False

        self.model = None
        self.last_date = None
        self.current_price = np.nan
        self.prob = None
        self.uncertainty = None

    def load_data(self, fred_api_key, start=pd.Timestamp.today()-pd.tseries.offsets.BDay(1500), end=pd.Timestamp.today()):
        if type(start) is int:
            start = end - pd.tseries.offsets.BDay(start)

        # load gold futures prices
        days_back_required = (pd.Timestamp.today()-start).round('D').days

        gold = Stock('GC=F').historical(days_back=days_back_required)
        gold['Date'] = pd.to_datetime(gold['Date'])
        gold['ClosingPrice'] = gold['Close']
        gold = gold.set_index('Date')[['ClosingPrice']]
        self.current_price = gold.ClosingPrice.values[-1]

        # load cpi and treasury yield
        fred = FredData(fred_api_key)
        cpi, treasury = fred.CPI(), fred.Treasury10Y()

        df = pd.merge_asof(gold.join(
            treasury), cpi, left_index=True, right_index=True, direction='nearest')
        df = df.dropna().loc[start.date():end.date()]
        self.df = df
        self.last_date = self.df.index[-1].strftime('%Y-%m-%d')

    def fit(self):
        if self.df is None:
            raise ValueError(
                'No data available. Please call load_data() before calling fit().')
        self.model = LinearRegressor(transform=np.log, invtransform=np.exp)
        X, y = self.df[['CPI', 'Treasury10Y']], self.df['ClosingPrice']
        self.model.fit(X, y, shift=-1)

        prediction, self.uncertainty = self.model.predict(X)
        self.df['Prediction'] = prediction

        # calculate probabilities
        diff = np.linspace(-350, 350, 1001)
        price = self.df.Prediction.values[-1] + diff
        self.prob = pd.DataFrame(self.uncertainty(
            diff), index=price, columns=['probability'])
        self.prob['pvalue'] = np.round([self.uncertainty.integrate_box_1d(
            p-self.current_price, np.inf) for p in price], 4)

    def display(self, return_figures=False):
        if not self.fitted:
            self.fit()

        # prob distribution
        fig1 = make_subplots(specs=[[{"secondary_y": True}]])
        fig1a = px.line(self.prob, y='pvalue')
        fig1b = px.line(self.prob, y='probability')
        fig1b.update_traces(yaxis="y2")

        fig1.add_traces(fig1a.data + fig1b.data)
        fig1.add_vline(self.current_price, line_color='red', annotation_text='Current Price')
        fig1.layout.xaxis.title = "Gold Price"
        fig1.layout.yaxis.title = "p-value"
        fig1.layout.yaxis2.title = "Probability"
        fig1.update_layout(
            title=f"R2={self.model.R2:.2f} (as of {self.last_date})", hovermode='x')
        fig1.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))

        # time series of predictions
        self.df['PredictedPrice'] = self.df.Prediction.shift(1)
        fig2 = px.line(self.df.dropna(), y=['PredictedPrice', 'ClosingPrice'])
        fig2.update_layout(xaxis_title='Time',
                           yaxis_title='Price', hovermode='x')
        if not return_figures:
            fig1.show(), fig2.show()
        else:
            return fig1, fig2
