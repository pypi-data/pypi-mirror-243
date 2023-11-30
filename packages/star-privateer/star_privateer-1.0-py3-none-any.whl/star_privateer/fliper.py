
'''
FliPer (Bugnet et al. 2018) implementation
for PLATO MSAP4-04 submodule.
'''

class FliPer :
  '''
  FliPer object, wrapping a random forest classifiers framework designed
  to analyse surface rotation in stellar light curves. 
  '''

  def __init__ (self, **kwargs) :
    '''
    Initiate a new FliPer instance. A ``FliPerLogg`` 
    classifier is created as attributes
    of the FliPer object. Additional parameters provided
    when initialising a FliPer instance will be passed
    to ``sklearn.ensemble.RandomForestClassifier``.
    '''
    self.FliPerLogg = RandomForestClassifier (**kwargs)
    self.__trained__ = False
    self.__tested__ = False
    self.__feature_names__ = None


  def train (self, target_id,  
             features, feature_names=None) :
    '''
    Train FliPer classifiers with the provided training set. 
    '''
    #TODO
    self.FliPerLogg.fit (X, Y)
    self.__trained__ = True
    self.__ntrainFliPerLogg__ = X.shape[0]
    if feature_names is not None :
      self.__feature_names__ = feature_names

  def test (self, target_id, features,
            feature_names=None) :
    '''
    Test FliPer classifiers with the provided test set. 
    '''
    #TODO
    if not self.__trained__ :
      raise Exception ("You must train your FliPer instance before testing it !")
    if feature_names is None :
      warnings.warn ('No feature_names provided, sanity check could not be performed.')
    elif np.any (feature_names!=self.__feature_names__) :
      raise Exception ('You did not provide the feature that were used to train FliPer !')
    self.__FliPerLoggTestScore__ = self.FliPerLogg.score (X, Y)
    predictedFliPerLogg = self.FliPerLogg.predict(X)
    self.__tested__ = True
    self.__ntestFliPerLogg__ = X.shape[0]

  def getNumberEltTrain (self) :
    '''
    Return a tuple of integer, corresponding to the number
    of elements used to train each FliPer classifier.
    '''
    if not self.__trained__ :
      raise Exception ("You must train your FliPer instance first !")
    return self.__ntrainFliPerLogg__

  def getNumberEltTest (self) :
    '''
    Return a tuple of integer, corresponding to the number
    of elements used to train each FliPer classifier.
    '''
    if not self.__tested__ :
      raise Exception ("You must use a test set with your FliPer instance first !")
    return self.__ntestFliPerLogg__ 

  def getFeatureNames (self) :
    '''
    Get name of feature that FliPer requires for classification.
    '''
    if self.__feature__names is None :
      warnings.warn ("Feature names have not been provided by the user, returning None.")
    return self.__feature_names__ 

  def getScore (self) :
    '''
    Returns FliPer classifying scores.  
    The FliPer instance must have been trained and tested before.
    '''
    if not self.__trained__ :
      raise Exception ("You must train and test your FliPer instance first !")
    if not self.__tested__ :
      raise Exception ("You must use a test set with your FliPer instance first !")
    return self.__FliPerLoggTestScore__

  def isTrained (self) :
    return self.__trained__

  def isTested (self) :
    return self.__tested__

  def analyseSet (self, features, feature_names=None) :
    '''
    Analyse provided targets using FliPer. 
    '''
    if feature_names is None :
      warnings.warn ('No feature_names provided, sanity check could not be performed.')
    elif np.any (feature_names!=self.__feature_names__) :
      raise Exception ('You did not provide the feature that were used to train FliPer !')
    logg = self.FliPerLogg.predict (features)
    return logg

  def save (self, filename) :
    '''
    Save the FliPer instance as ``filename``.
    '''
    with open (filename, 'wb') as f :
      pickle.dump (self, f)
