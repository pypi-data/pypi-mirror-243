from operator import index
import numpy as np
import pandas as pd
import os

from .models import *

def load(path, separator = "\t", skipr = 0, naFilter = False, index_gene = -1, index_lengths = -1, head = None) -> pd.DataFrame:
    """
    Load any data from a txt or csv file. (Reuse function)
    
    :param file_path: The path where the file is stored.
    :type file_path: str
        
    :param separator: An attribute indicating how the columns of the file are separated.
    :type separator: str,optional
         
    :param skipr: Number of rows the user wishes to omit from the file, defaults to 0.
    :type skipr: int, optional
    
    :param naFilter: Boolean to detect NA values in a file. NA values shall be replaced by 0's, defaults to False.
    :type naFilter: boolean, optional
    
    :param index_gene: Column position where the gene names are stored in the dataset, defaults to -1 (deactivated).
    :type index_gene: int, optional
    
    :param index_lengths: Column position where the gene lengths are store in the dataset, defaults to -1 (deactivated).
    :type index_lengths: int, optional
    
    :param head: Row number(s) containing column labels and marking the start of the data (zero-indexed), defaults to None.
    :type head: int, optional
        
    :return: A dataset object from the reading of a file
    :rtype: :class:`bioscience.base.models.Dataset`
    """
    dataset = None
    if path is not None:
        extensionsCsv = [".txt",".csv"]    
        fileName, fileExtension = os.path.splitext(path)
        if fileExtension in extensionsCsv:
            if naFilter is True:
                dfPandas = pd.read_csv(path, sep=separator, skiprows = skipr, na_filter=naFilter, header = head).fillna(0)
            else:
                dfPandas = pd.read_csv(path, sep=separator, skiprows = skipr, header = head)
            
            dataColumns = np.asarray(dfPandas.columns)
            dataset = np.asarray(dfPandas)
            # Dataset object
            geneNames = None
            lengths = None
            
            # Get gene names from dataset
            if index_gene >= 0:
                index_lengths = index_lengths -1 # Update gene lengths index due to remove the gene column of the dataset.
                geneNames = dataset[:,index_gene]
                dataset = np.delete(dataset, index_gene, 1)                
            
            # Get lengths from dataset
            if index_lengths >= 0:
                lengths = dataset[:,index_lengths]
                dataset = np.delete(dataset, index_lengths, 1)
                
            
            dataColumns = np.delete(dataColumns, np.arange(0, 1 + index_gene))         
            return Dataset(dataset.astype(np.double), geneNames=geneNames, columnsNames=dataColumns, lengths=lengths)
        else:
            return None

def saveResultsIndex(path, models):    
    """
    Save the results index (rows and columns index of the dataset) of applying a data mining technique.
    
    :param path: The path where the file will be stored.
    :type path: str
        
    :param models: An attribute indicating how the columns of the file are separated.
    :type models: :class:`bioscience.dataMining.biclustering.BiclusteringModel`
         
    """
    if models is not None:
        iLevel = 1     
        for model in models:
            infoData = []
            for oBicluster in model.results:
                if oBicluster.rows is not None:
                    rows = ','.join(str(int(row)) for row in oBicluster.rows)
                else:
                    rows = ""
                
                if oBicluster.cols is not None:
                    cols = ','.join(str(int(col)) for col in oBicluster.cols)
                else:
                    cols = ""
                
                infoData.append(rows + ';' + cols)
            
            df = pd.DataFrame(infoData, columns=['Data'])
            df['Data'] = df['Data'].str.replace('"', '')
            df.to_csv(path+"index"+str(iLevel)+".csv", index=False, header=False)
            iLevel += 1
    
        print("Results index saved in: " + path)

def saveResults(path, models, data):
    """
    Save the results of applying a data mining technique.
    
    :param path: The path where the file will be stored.
    :type path: str
        
    :param models: The results of the data mining technique.
    :type models: :class:`bioscience.dataMining.biclustering.BiclusteringModel`
    
    :param data: The dataset object which stores the original dataset.
    :type data: :class:`bioscience.base.models.Dataset`
         
    """
    if models is not None:
        iLevel = 1
        for i, model in enumerate(models, start=1):
            infoModel = ""
            for j, oBicluster in enumerate(model.results, start=1):
                if isinstance(data, set):
                    geneNames = list(data)[iLevel-1].geneNames
                    colNames = list(data)[iLevel-1].columnsNames
                else:
                    geneNames = data.geneNames
                    colNames = data.columnsNames
                
                if oBicluster.rows is not None:
                    if geneNames is not None:
                        rows = ','.join(str(geneNames[int(row)]) for row in oBicluster.rows)
                    else:
                        rows = ','.join(str(row) for row in oBicluster.rows)
                else:
                    rows = ""
                
                if oBicluster.cols is not None:
                    if colNames is not None:
                        cols = ','.join(str(colNames[int(col)]) for col in oBicluster.cols)
                    else:
                        cols = ','.join(str(int(col)) for col in oBicluster.cols)
                else:
                    cols = ""
                
                infoBicluster = f"\nRESULT #{j} (ROWS: {rows}) - (COLS: {cols})\n"
                   
                if isinstance(data, set):
                    dataset = list(data)[i - 1].original
                else:
                    dataset = data.original
                for oRow in oBicluster.rows:
                    if oBicluster.cols is not None:
                        infoBicluster += ",".join(str(dataset[int(oRow)][int(oCol)]) for oCol in oBicluster.cols)
                        infoBicluster += "\n"

                infoModel += infoBicluster

            df = pd.DataFrame([infoModel], columns=['Data'])
            df['Data'] = df['Data'].str.replace('"', '')
            df.to_csv(f"{path}results{i}.csv", index=False, header=False)
            iLevel += 1

        print("Results saved in: " + path)
        
def saveGenes(path, models, data):
    """
    Save the gene names from the results of applying a data mining technique.
    
    :param path: The path where the file will be stored.
    :type path: str
        
    :param models: The results of the data mining technique.
    :type models: :class:`bioscience.dataMining.biclustering.BiclusteringModel`
    
    :param data: The dataset object which stores the original dataset.
    :type data: :class:`bioscience.base.models.Dataset`
         
    """
    if models is not None:
        iLevel = 1
        for model in models:
            if isinstance(data, set):
                geneNames = list(data)[iLevel-1].geneNames
            else:
                geneNames = data.geneNames
            
            infoData = []
            for oBicluster in model.results:
                if geneNames is not None:
                    rows = ','.join(str(geneNames[int(row)]) for row in oBicluster.rows)
                else:
                    rows = ','.join(str(row) for row in oBicluster.rows)
                infoData.append(rows)
            
            df = pd.DataFrame(infoData, columns=['Data'])
            df['Data'] = df['Data'].str.replace('"', '')
            df.to_csv(path+"genes"+str(iLevel)+".csv", index=False, header=False)
            iLevel += 1

    print("Genes saved in: " + path)

def saveBinaryDatasets(path, datasets):
    """
    If the dataset has been binarised, this function allows storing the binary dataset.
    
    :param path: The path where the file will be stored.
    :type path: str
        
    :param datasets: The dataset object which stores the binary dataset.
    :type datasets: :class:`bioscience.base.models.Dataset`
         
    """
    if datasets is not None:
        if isinstance(datasets, set):
            iLevel = 1
            for dataset in datasets:
                df = pd.DataFrame(dataset.data)
                df.to_csv(path+"dataset"+str(iLevel)+".csv", index=False, header=False)
                iLevel += 1
        else:
            df = pd.DataFrame(datasets.data)
            df.to_csv(path+"dataset.csv", index=False, header=False)
        
        print("Binary datasets saved in: " + path)


        
        
        
    
    