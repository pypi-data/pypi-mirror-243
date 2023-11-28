from sklearn import preprocessing
from bioscience.base import *
import numpy as np
    
def binarize(dataset, threshold = 0.0, soc = None):
    """
    Applying binarisation to a dataset
    
    :param dataset: The dataset object to be binarized.
    :type dataset: :class:`bioscience.base.models.Dataset`
    
    :param threshold: Feature values below or equal to this are replaced by 0, above it by 1. Threshold may not be less than 0 for operations on sparse matrices, defaults to 0.0
    :type threshold: float, optional
    
    :param soc: Threshold representing the number of ones each row of the dataset should have as a minimum. If a row does not exceed this threshold, it shall be removed from the dataset, defaults to None.
    :type soc: int, optional        
    """ 
    if dataset is not None:
        dataset.data = np.array(preprocessing.binarize(dataset.data, threshold = threshold))
        if soc is not None:
            __removeRows(dataset,soc)
        dataset.data = dataset.data.astype(np.uint64)


def binarizeLevels(dataset, inactiveLevel = None, activeLevel = None, cut = 0.5, step = 0.1, soc = None):
    
    """
    Generate multiple binary datasets by applying fuzzy logic.
    
    :param dataset: The dataset object to be binarized.
    :type dataset: :class:`bioscience.base.models.Dataset`
    
    :param inactiveLevel: If an element in the dataset is below this threshold it is considered an inactive gene (value equal to 0 in a binarised dataset).
    :type inactiveLevel: float, optional
    
    :param activeLevel: If an item in the dataset is above this threshold it is considered an active gene (value equal to 1 in a binarised dataset).
    :type activeLevel: float, optional
    
    :param cut: Value used in fuzzy logic to determine up to which value an active gene is to be considered. This value will assist in the creation of multiple binarised datasets.
    :type cut: float, optional
    
    :param step: Value used in fuzzy logic to determine how much the value in fuzzy logic should be lowered for each binary dataset generated. This value will assist in the creation of multiple binarised datasets.
    :type step: float, optional    
    
    :param soc: Threshold representing the number of ones each row of the dataset should have as a minimum. If a row does not exceed this threshold, it shall be removed from the dataset, defaults to None.
    :type soc: int, optional        
    """ 
    
    if dataset is not None:
        # Column means
        colMeans = np.mean(dataset.data, axis = 0)
        
        # Standard deviation
        colDeviation = np.std(dataset.data, axis = 0)
        
        # 3) Calc z value gaussian distribution   
        if inactiveLevel is not None and activeLevel is not None:
            
            # Calc Z values
            for (rowIndex, rowCol), value in np.ndenumerate(dataset.data):
                dataset.data[rowIndex][rowCol] = (value - colMeans[rowCol]) / colDeviation[rowCol]
            
            # Binarize matrix with Z values
            __binarizeLevelsMatrix(dataset.data, inactiveLevel, activeLevel)
            
        else:
            
            # Binarize matrix without Z values and remove rows whose sum of one-values is less than the SOC parameter
            __binarizeLevelsMatrix(dataset.data, colMeans, colDeviation)
        
        # Build binary matrices and remove rows whose sum of one-values is less than the SOC parameter
        listDataset = __buildBinaryMatrices(dataset, cut, step, soc)
                
        return listDataset        
    else:
        return None

def __binarizeLevelsMatrix(data, inactiveLevel = None, activeLevel = None, colMeans = None, colDeviation = None):
    
    if inactiveLevel is not None and activeLevel is not None: # Binarize matrix with Z values
        slope = 1 / (activeLevel - inactiveLevel)
        secEquation = slope * inactiveLevel * -1
        
        np.place(data, data<=inactiveLevel, [0])
        np.place(data, data>=activeLevel, [1])
        np.place(data, np.logical_and(data>inactiveLevel, data < activeLevel), [(slope*data) + secEquation])
    
    else: # Binarize matrix without Z values
        for (rowIndex, rowCol), value in np.ndenumerate(data):
            cutOffMin = colMeans[rowCol] - colDeviation[rowCol]
            cutOffMax = colMeans[rowCol] + colDeviation[rowCol]   
            slope = 1 / (cutOffMax - cutOffMin) 
            secEquation = slope * cutOffMin * -1
            
            np.place(data, data <= cutOffMin, [0])  
            np.place(data, data >= cutOffMax, [1])      
            np.place(data, np.logical_and(data > cutOffMin,data < cutOffMax), [(slope*data) + secEquation])
    
    return data

def __buildBinaryMatrices(dataset, cut, step, soc):
    
    listData = set()
    if cut is not None:
        limit = 1.0
        while(limit >= cut):
            dataAux = geneNamesAux = lengthsAux = annotationsAux = None
            
            dataAux = np.copy(dataset.data)
            if dataset.geneNames is not None: 
                geneNamesAux = np.copy(dataset.geneNames)
            
            if dataset.lengths is not None:
                lengthsAux = np.copy(dataset.lengths)
            
            if dataset.annotations is not None:
                annotationsAux = np.copy(dataset.annotations)
            
            np.place(dataAux, dataAux>=limit, [1])
            np.place(dataAux, np.logical_and(np.logical_and(dataAux<limit,dataAux != 0),dataAux != 1), [0])
            if soc is not None:
                if geneNamesAux is not None:
                    geneNamesAux = np.delete(geneNamesAux,np.where(np.sum(dataAux, axis = 1) <= soc)[0], axis=0) # Remove rows whose sum of one-values is less than the SOC parameter.  
                
                if lengthsAux is not None:
                    lengthsAux = np.delete(lengthsAux,np.where(np.sum(dataAux, axis = 1) <= soc)[0], axis=0) # Remove rows whose sum of one-values is less than the SOC parameter.  
                
                if annotationsAux is not None:
                    annotationsAux = np.delete(annotationsAux,np.where(np.sum(dataAux, axis = 1) <= soc)[0], axis=0) # Remove rows whose sum of one-values is less than the SOC parameter.  
                
                dataAux = np.delete(dataAux,np.where(np.sum(dataAux, axis = 1) <= soc)[0], axis=0) # Remove rows whose sum of one-values is less than the SOC parameter.  
            
            dataObject = Dataset(dataset.original, geneNames=geneNamesAux, lengths=lengthsAux, annotations=annotationsAux, cut=limit)
            dataObject.data = dataAux
            dataObject.data = dataObject.data.astype(np.uint64)
            listData.add(dataObject)
            limit -= step
    else:
        dataset.data = dataset.data.astype(np.uint64)
        listData.add(dataset)
    
    return listData

def __removeRows(dataset, soc):
    dataset.original = np.delete(dataset.original,np.where(np.sum(dataset.data, axis = 1) <= soc)[0], axis=0) # Remove rows whose sum of one-values is less than the SOC parameter.            
            
    if dataset.geneNames is not None:
        dataset.geneNames = np.delete(dataset.geneNames,np.where(np.sum(dataset.data, axis = 1) <= soc)[0], axis=0) # Remove rows whose sum of one-values is less than the SOC parameter.            
    
    if dataset.lengths is not None:
        dataset.lengths = np.delete(dataset.lengths,np.where(np.sum(dataset.data, axis = 1) <= soc)[0], axis=0) # Remove rows whose sum of one-values is less than the SOC parameter.            
                
    if dataset.annotations is not None:
        dataset.annotations = np.delete(dataset.annotations,np.where(np.sum(dataset.data, axis = 1) <= soc)[0], axis=0) # Remove rows whose sum of one-values is less than the SOC parameter.            
    
    dataset.data = np.delete(dataset.data,np.where(np.sum(dataset.data, axis = 1) <= soc)[0], axis=0) # Remove rows whose sum of one-values is less than the SOC parameter.                        