
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


class SqrtTransformer(BaseEstimator, TransformerMixin):
    """Applique la transformation racine carrée aux variables d'entrée"""

    def __init__(self):
        pass

    def fit(self, X, y=None):
        """Rien à faire ici"""
        return self

    def transform(self, X, y=None):
        """Applique la transformation racine carrée aux variables d'entrée"""
        return np.sqrt(X)
