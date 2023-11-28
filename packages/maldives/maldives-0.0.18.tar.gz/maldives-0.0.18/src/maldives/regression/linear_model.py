from sklearn.linear_model import HuberRegressor
from scipy.stats import gaussian_kde


def _shift_data(X, y, n):
    # +ve: features predict previous value, -ve: features predict next value
    if n == 0:
        return X, y
    return (X[n:], y[:-n]) if n > 0 else (X[:n], y[-n:])


class LinearRegressor(object):
    def __init__(self, fitter=HuberRegressor(), transform=None, invtransform=None):
        """Basic linear regression model with historical uncertainty

        Args:
            fitter (scikit-learn model, optional): Model object with fit(), predict() and score(). Defaults to HuberRegressor().
            transform (Function, optional): Transformation applied to data, e.g. log. Defaults to None.
            invtransform (Function, optional): Function to invert transform, e.g. exp. Defaults to None.
        """
        self.fitter = fitter
        identity = (lambda x: x)
        self.transform = identity if transform is None else transform
        self.invtransform = identity if invtransform is None else invtransform
        self.uncertainty = None
        self.R2 = 0
        self.shift = 0

    def fit(self, X, y, shift=0, **kwargs):
        """Fit linear model to data

        Args:
            X (array): features
            y (array): response
            shift (int, optional): shift in y. Positive means current features are used to predict previous response. 
            Negative means current features are used to predict next response. Defaults to 0.

        Returns:
            prediction (array): predicted response
            uncertainty (scipy.gaussian_kde): historical uncertainty distribution
            score (float): goodness of fit (R-squared)
        """
        self.shift = shift
        X, y = _shift_data(X, y, shift)
        X_transformed = self.transform(X)
        y_transformed = self.transform(y)
        self.fitter.fit(X_transformed, y_transformed, **kwargs)
        prediction = self.invtransform(self.fitter.predict(X_transformed))

        # record uncertainty from the fit
        self.uncertainty = gaussian_kde(prediction-y)
        self.R2 = self.fitter.score(X_transformed, y_transformed)

        return prediction, self.uncertainty, self.R2

    def predict(self, X, **kwargs):
        """Predict on feature.

        Args:
            X (array): features

        Returns:
            prediction (array): predicted response
            uncertainty (scipy.gaussian_kde): historical uncertainty distribution
        """
        return self.invtransform(self.fitter.predict(self.transform(X), **kwargs)), self.uncertainty
