## cmm.py
## ==
## Correlation Matrix Memory class
## ==
## author: Dr James Stovold
## date  : Jun 04, 2022
## ==
##
## N.B. based on C++ version available under native/src/CDMSim/cmm.{cpp,h}; this implementation mirrors that directly, which 
## is why it doesn't look particularly "python"-esque
##
## The training set consists of k Input-Output pairs, {Ik, Ok}, which are logical-OR'd together to form the corresponding
## associations in M.
##
##
##
##  [    ]  [             ]
##  [    ]  [             ]
##  [ Ik ]  [      M      ]
##  [    ]  [             ]
##  [    ]  [             ]
##  [    ]  [             ]
##
##          [      Ok     ]
##
## As the k Input-Output pairs are presented to the network, building up the associations in the matrix, M.
## Upon recall, we get: O = MIr, where Ir is the input pattern, and O is the output from the network trained with M.
## The desired output pattern, Or, is currently combined with noise from other patterns stored in the network, er, hence:
##     O = Or + er
##    er = sum_{k=1;k!=r}^N (I^T_k.I_r).Ok
## By thresholding the output, O, to an appropriate (!) level, we can retrieve the desired output pattern, Or.
##
## ==

class cmm():
  _M       = None
  _inputs  = 0
  _outputs = 0

  def __init__(self, numInputs, numOutputs):
    self._inputs  = numInputs
    self._outputs = numOutputs
    self._M = [False] * self._inputs * self._outputs

  def addAssociation(self, Ik, Ok):
    for i in range(self._inputs):
      if Ik[i]:
        for o in range(self._outputs):
          if Ok[o]:
            self._M[i * self._outputs + o] = true

  def recall(self, Ir):
    outputArr = [False] * self._outputs
    for o in range(self._outputs):
      sum = 0
      for i in range(self._inputs):
        sum += Ir[i] * self._M[i * self._outputs + o]
      outputArr[o] = sum
    return outputArr

  def thresholdResults(self, O, theta, invert=False):
    outputArr = [False] * self._outputs
    if !invert:
      for o in range(self._outputs):
        outputArr[o] = (O[o] <= -theta)
    else:
      for o in range(self._outputs):
        outputArr[o] = (O[o] >= theta)
    return outputArr

  def invertVectorInPlace(self, v):
    # probably doesn't actually invert in place but the C++ method was called this
    return [x ^ True for x in v]
    


