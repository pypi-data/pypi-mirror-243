import numpy as np

def tpm(dataset):
    """
    Apply TPM (transcripts-per-million) method preprocessing to a dataset
    
    :param dataset: The dataset object to be preprocess.
    :type dataset: :class:`bioscience.base.models.Dataset`
        
    """    
    if dataset is not None and dataset.lengths is not None:
        
        countsLib = np.zeros((len(dataset.data),len(dataset.data[0])))
        for (rowIndex, rowCol), value in np.ndenumerate(dataset.data):
            countsLib[rowIndex][rowCol] = (value / dataset.lengths[rowIndex]) * 1000000
        
        colSums = np.zeros(len(dataset.data[0]))
        for (rowIndex, rowCol), value in np.ndenumerate(countsLib):                
            colSums[rowCol] += value
            
        for (rowIndex, rowCol), value in np.ndenumerate(countsLib):
            countsLib[rowIndex][rowCol] = (value * 1000000) / colSums[rowCol]  

        dataset.data = countsLib

def fpkm(dataset):
    """
    Apply FPKM (transcript per million mapped reads) method preprocessing to a dataset
    
    :param dataset: The dataset object to be preprocess.
    :type dataset: :class:`bioscience.base.models.Dataset`
        
    """    
    if dataset is not None and dataset.lengths is not None:
        
        colSums = np.zeros(len(dataset.data[0]))
        for (rowIndex, rowCol), value in np.ndenumerate(dataset.data):                
            colSums[rowCol] += value
        
        countsLib = np.zeros((len(dataset.data),len(dataset.data[0])))
        for (rowIndex, rowCol), value in np.ndenumerate(dataset.data):
            countsLib[rowIndex][rowCol] = (value / (dataset.lengths[rowIndex] * colSums[rowCol])) * 1000000000
            
        dataset.data = countsLib

def cpm(dataset):
    """
    Apply CPM (counts per million) method preprocessing to a dataset
    
    :param dataset: The dataset object to be preprocess.
    :type dataset: :class:`bioscience.base.models.Dataset`
        
    """ 
    if dataset is not None:
        
        colSums = np.zeros(len(dataset.data[0]))
        for (rowIndex, rowCol), value in np.ndenumerate(dataset.data):                
            colSums[rowCol] += value
        
        countsLib = np.zeros((len(dataset.data),len(dataset.data[0])))
        for (rowIndex, rowCol), value in np.ndenumerate(dataset.data):
            countsLib[rowIndex][rowCol] = (value / colSums[rowCol]) * 1000000
            
        dataset.data = countsLib