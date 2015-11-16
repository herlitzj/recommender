import numpy as np

"""
X = np.array([ [0,0,1,],[0,1,1],[1,0,1],[1,1,1] ])
Y = np.array([[0,1,1,0]]).T
synapse0 = 2*np.random.random((3,4)) - 1
synapse1 = 2*np.random.random((4,1)) - 1
for j in xrange(1000):
	level1 = 1/(1+np.exp(-(np.dot(X, synapse0))))
	level2 = 1/(1+np.exp(-(np.dot(level1,synapse1))))
	level2_delta = (Y - level2)*(level2*(1-level2))
	level1_delta = level2_delta.dot(synapse1.T)*(level1 *(1-level1))
	synapse1 += level1.T.dot(level2_delta)
	synapse0 += X.T.dot(level1_delta)
	print level1
"""

# sigmoid function
def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))
    
# input dataset
X = np.array([  [0,0,1],
                [0,1,1],
                [1,0,1],
                [1,1,1] ])
    
# output dataset            
y = np.array([[0,1,1,0]]).T

# seed random numbers to make calculation
# deterministic (just a good practice)
np.random.seed(1)

# initialize weights randomly with mean 0
syn0 = 2*np.random.random((3,1)) - 1
print syn0
print
for iter in xrange(10000):

    # forward propagation
    l0 = X
    l1 = 1/(1+np.exp(-(np.dot(l0,syn0))))
#    print l0
#    print l1
#    print
    # how much did we miss?
    l1_error = y - l1
#    print l1_error
#    print
    # multiply how much we missed by the 
    # slope of the sigmoid at the values in l1
    l1_delta = l1_error * (l1*(1-l1))
#   print l1_delta
#    print
    # update weights
    syn0 += np.dot(l0.T,l1_delta)
#    print syn0
#    raw_input()
print "Output After Training:"
print l1
print syn0
