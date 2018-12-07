# Some functions for Usage.py

import GenerativeModel as gm
import NeuralNetwork as nn
import numpy as np
import matplotlib.pyplot as plt
import KalmanSmoother as ks

# modelType can be 'LG'/'NLG'/'LNG'/'NLNG'
def trainCnnPointEstimator(modelType):
  hidden,measure = gm.loadData('Generated.Data/' + modelType + '.Train')
  testHidden, testMeasure = gm.loadData('Generated.Data/' + modelType + '.Test')
  cnnPointEstimator = nn.CnnPointEstimator(hidden.shape[1])
  cnnPointEstimator.train(2e-4,100,200,measure,hidden,
    'Trained.Models/CNN.Point.Estimator.' + modelType + '.ckpt',testMeasure,
    testHidden,1213,showKalman=(modelType=='LG'))   

# modelType can be 'LG'/'NLG'/'LNG'/'NLNG'
def testCnnPointEstimator(modelType):
  testHidden,testMeasure = gm.loadData('Generated.Data/' + modelType + '.Test')
  cnnPointEstimator = nn.CnnPointEstimator(testHidden.shape[1])
  sampleNo = 1213
  estimated = cnnPointEstimator.infer(testMeasure[sampleNo],
    'Trained.Models/CNN.Point.Estimator.' + modelType + 
    '/CNN.Point.Estimator.' + modelType + '.ckpt')
  loss = cnnPointEstimator.computeLoss(estimated,testHidden[sampleNo],
    'Trained.Models/CNN.Point.Estimator.' + modelType + 
    '/CNN.Point.Estimator.' + modelType + '.ckpt')
  if modelType=='LG':
    testKalmanZ,dump = ks.loadResults('Results.Data/' + modelType + 
      '.Kalman.Results')
  plt.figure(figsize=(10,5))
  plt.scatter(np.arange(testHidden.shape[1]),testHidden[sampleNo],
    marker='o',color='blue',s=4)
  if modelType=='LG': plt.plot(testKalmanZ[sampleNo],color='green')
  plt.plot(estimated.flatten(),color='red')
  plt.show()