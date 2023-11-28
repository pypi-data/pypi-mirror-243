import numpy as np

class Dataset:
    """
    This is a concept class representing a dataset.
    
    :param original: Here the original dataset is stored in a NumPy array.
    :type original: np.array
        
    :param data: This attribute is used to store the dataset once it has undergone the transformations desired by the user.
    :type data: np.array
         
    :param geneNames: Array with the name of the genes involved in the dataset. If the dataset does not have the name of the genes, it shall be replaced by a set of sequential numbers.
    :type geneNames: np.array, optional
    
    :param columnsNames: Array with the name of the columns involved in the dataset. If the dataset does not have the name of the columns, it shall be replaced by a set of sequential numbers.
    :type columnsNames: np.array, optional
    
    :param lengths: Array with gene length value (RNA-Seq)
    :type lengths: np.array, optional    
    
    :param annotations: Array that stores data from an annotation file for subsequent validation phases.
    :type annotations: np.array, optional
    
    :param cut: Cut-off parameter used in level binarisation.
    :type cut: float, optional
    
    """    
    
    def __init__(self, data, geneNames = None, columnsNames = None, lengths = None, annotations = None, cut = None):
        """
        Constructor method
        """
        self._original = data
        self._data = np.copy(self.original)
        self._geneNames = geneNames
        self._lengths = lengths
        self._annotations = annotations
        self._cut = cut
        self._columnsNames = columnsNames
    
    @property
    def data(self):
        """
        Getter and setter methods of the data property.
        """
        return self._data
    
    @data.setter
    def data(self, data):
        self._data = data
    
    @property
    def geneNames(self):
        """
        Getter and setter methods of the geneNames property.
        """
        return self._geneNames
    
    @geneNames.setter
    def geneNames(self, geneNames):
        self._geneNames = geneNames
    
    @property
    def lengths(self):
        """
        Getter and setter methods of the lengths property.
        """
        return self._lengths
    
    @lengths.setter
    def lengths(self, lengths):
        self._lengths = lengths
    
    @property
    def annotations(self):
        """
        Getter and setter methods of the annotations property.
        """
        return self._annotations
    
    @annotations.setter
    def annotations(self, annotations):
        self._annotations = annotations
    
    @property
    def cut(self):
        """
        Getter and setter methods of the cut property.
        """
        return self._cut
    
    @cut.setter
    def cut(self, cut):
        self._cut = cut
    
    @property
    def original(self):
        """
        Getter and setter methods of the original property.        
        """
        return self._original
    
    @original.setter
    def original(self, original):
        self._original = original
    
    @property
    def columnsNames(self):
        """
        Getter and setter methods of the columnsNames property.
        """
        return self._columnsNames
    
    @columnsNames.setter
    def columnsNames(self, columnsNames):
        self._columnsNames = columnsNames
    
    def __eq__(self, other):
        if isinstance(other, Dataset):
            return np.array_equal(self.data,other.data)
        else:
            return False
    
    def __hash__(self):
        return 1

class Validation:
    """
    This is a conceptual class representing a validation model after applying a data mining technique.
    
    :param measure: Name of the validation measure used.
    :type measure: str
        
    :param value: Value of the validation measure used.
    :type value: float
        
    """
    
    def __init__(self, measure, value):
        """
        Constructor method
        """
        self._measure = measure
        self._value = value
    
    @property
    def measure(self):
        """
        Getter and setter methods of the measure property.
        """
        return self._measure
    
    @measure.setter
    def measure(self, measure):
        self._measure = measure
    
    @property
    def value(self):
        """
        Getter and setter methods of the value property.
        """
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
    
    def __eq__(self, other):
        if isinstance(other, Validation):
            return self.measure == other.measure
        else:
            return False
    
    def __hash__(self):
        return hash(self.measure)
    
    def __str__(self):
        return 'Measure (0): (1)'.format(self.measure, self.value)

class Bicluster:
    """
    This is a conceptual class representing a bicluster after applying a Biclustering technique.
    
    :param rows: Rows of the bicluster.
    :type rows: np.array
        
    :param cols: Columns of the bicluster.
    :type cols: np.array, optional
    
    :param data: Bicluster values according to the original dataset.
    :type data: np.array, optional
    
    :param validations: A set of instances from :class:`bioscience.base.models.Validation`.
    :type validations: np.array, optional
    
    """
    
    def __init__(self, rows, cols = None, data=None, validations=None):
        """
        Constructor method
        """
        self._rows = rows
        self._cols = cols
        self._data = data        
        self._validations = validations
    
    @property
    def rows(self):
        """
        Getter and setter methods of the rows property.
        """
        return self._rows
    
    @rows.setter
    def rows(self, rows):
        self._rows = rows
    
    @property
    def cols(self):
        """
        Getter and setter methods of the cols property.
        """
        return self._cols
    
    @cols.setter
    def cols(self, cols):
        self._cols = cols
    
    @property
    def data(self):
        """
        Getter and setter methods of the data property.
        """
        return self._data
    
    @data.setter
    def data(self, data):
        self._data = data
        
    @property
    def validations(self):
        """
        Getter and setter methods of the validations property.
        """
        return self._validations
    
    @validations.setter
    def validations(self, validations):
        self._validations = validations
        
    def sizeBicluster(self):
        """
        Number of total elements in the bicluster.
        """
        return len(self.rows) * len(self.cols)
    
    def sort(self):
        """ 
        Sort the column and row array by theirs indices.
        """
        self.rows.sort()
        self.cols.sort()
    
    def __str__(self):
        return 'Bicluster: rows{0} - cols{1}'.format(self.rows,self.cols)

class BiclusteringModel:
    
    """
    This is a conceptual class representing a set of biclusters generated after applying a Biclustering technique.
    
    :param results: Data structure (set) that stores all biclusters after running a Biclustering algorithm.
    :type results: set(:class:`bioscience.base.models.Bicluster`), optional
        
    :param executionTime: Time taken to execute the Biclustering method.
    :type executionTime: float, optional
    
    """
    
    def __init__(self, results = None):     
        """
        Constructor method
        """   
        if results is not None and all(isinstance(bic, Bicluster) for bic in results):
            self._results = results
        else:
            self._results = set()
        
        self._executionTime = 0
    
    @property
    def executionTime(self):
        """
        Getter and setter methods of the executionTime property.
        """
        return self._executionTime
    
    @executionTime.setter
    def executionTime(self, executionTime):
        self._executionTime = executionTime
    
    @property
    def results(self):
        """
        Getter and setter methods of the results property.
        """
        return self._results
    
    @results.setter
    def results(self, results):
        self._results = results
    
    def __str__(self):
        return '\n'.join(str(bic) for bic in self.results)