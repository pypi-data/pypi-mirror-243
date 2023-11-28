from sklearn import preprocessing
import numpy as np
import pandas as pd
import math

def discretize(dataset, n_bins = 2, strategy = 'kmeans'):
    """
    Discretizes data into N bins.
    
    :param dataset: The dataset object to be discretized.
    :type dataset: :class:`bioscience.base.models.Dataset`
    
    :param n_bins: Number of bins to produce, defaults to 2.
    :type n_bins: int, optional
    
    :param strategy: Strategy used to define the widths of the bins. Options (kmeans, quantile, uniforme). Defaults to 'kmeans'.
    :type strategy: str, optional
        
    """
    if dataset is not None and n_bins > 1:
        dataset.data = np.array(preprocessing.KBinsDiscretizer(n_bins, encode = 'ordinal', strategy = strategy).fit_transform(dataset.data))

def standardize(dataset):
    """
    Standardize a dataset
    
    :param dataset: The dataset object to be standarized.
    :type dataset: :class:`bioscience.base.models.Dataset`
        
    """
    if dataset is not None:
        dataset.data = np.array(preprocessing.StandardScaler().fit_transform(dataset.data))

def scale(dataset):
    """
    Scale a dataset
    
    :param dataset: The dataset object to be scaled.
    :type dataset: :class:`bioscience.base.models.Dataset`
        
    """
    if dataset is not None:
        dataset.data = np.array(preprocessing.MinMaxScaler().fit_transform(dataset.data))

def normalDistributionQuantile(dataset, quantiles = 1000):
    """
    Use Normal Distribution Quantile to preprocess a dataset.
    
    :param dataset: The dataset object to be normal distribution quantile.
    :type dataset: :class:`bioscience.base.models.Dataset`
    
    :param quantiles: Number of quantiles to be computed., defaults to 1000.
    :type quantiles: int, optional        
    """
    if dataset is not None:
        dataset.data = np.array(preprocessing.QuantileTransformer(n_quantiles=quantiles, output_distribution='normal').fit_transform(dataset.data))