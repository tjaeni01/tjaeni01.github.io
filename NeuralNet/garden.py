# Tucker Jaenicke
# AI HW4

import numpy as np
import csv
import random


# sigmoid activation function
def sigmoid(s):
	return 1/(1+np.exp(-s))

#derivative of sigmoid function
def sigmoid_deriv(s):
	return s * (1 - s)

class Neural_Network(object):
	# define initialization of NN
	def __init__(self):
	    #parameters
		self.inputSize = 4
		self.outputSize = 3
		self.hiddenSize = 3

	    #initialize random weights
	    #weights from input to hidden layer
		self.w1 = np.random.randn(self.inputSize, self.hiddenSize)
		# weights from hidden to output layer
		self.w2 = np.random.randn(self.hiddenSize, self.outputSize)

	# feed forward algorithm
	def forward(self, X):
		# multiply the first weights then use activation function
		self.z1 = np.dot(X, self.w1)
		self.z2 = sigmoid(self.z1)
		# multiple the second weights then use activation function
		self.z3 = np.dot(self.z2, self.w2)
		pred = sigmoid(self.z3)
		return pred

	# backward propagation algorithm
	def backward(self, X, y, pred):
		#calculate the prediction error
		self.pred_error = y - pred
		#apply derivative of activation function
		self.pred_delta = 0.1*self.pred_error * sigmoid_deriv(pred)

		# multiply weights by error to get contribution of weights to error
		self.z2_error = self.pred_delta.dot(self.w2.T)
		#apply derivative of activation function
		self.z2_delta = self.z2_error * sigmoid_deriv(self.z2)

		#adjust weights accordingly
		self.w1 += X.T.dot(self.z2_delta)
		self.w2 = self.z2.T.dot(self.pred_delta)

	#train the NN by feeding forward then back propagating
	def train(self, X, y):
		pred = self.forward(X)
		self.backward(X, y, pred)

	# shows the input test set and its prediction
	def predict(self):
		print("Predicted data based on trained weights: ")
		print("Input (scaled): \n" + str(X_test))
		print("Output: \n" + str(self.forward(X_test)))

	# returns the accuracy of the NN on the test set
	def accuracy(self, X_test, y_test):
		#get the predicted values
		y_pred = self.forward(X_test)
		length, col = y_pred.shape
		score = 0
		# increment score for every correct prediction
		for i in range(length):
			if np.argmax(y_pred[i]) == np.argmax(y_test[i]):
				score += 1
		return score/length


# read in data
with open('Iris_data.txt', newline='') as csvfile:
    data = list(csv.reader(csvfile))
# convert list to np array
data = np.array(data)
#shuffle array
np.random.shuffle(data)


# separate features  from labels
X = data[:,:-1].astype(np.float)
y_cat = data[:,-1:]

#normalize data to be between -6 and 6
for i in range(len(X[0])):
	X[:,0] = X[:,i]/np.amax(X[:,i], axis=0) * 12 - 6

# convert categorical labels to binary labels
# makes output size three, with a one-hot representation
y = np.zeros((y_cat.size, 3))
for i in range(y_cat.size):
	if y_cat[i] == "Iris-setosa":
		y[i][0] = 1.0
	elif y_cat[i] == "Iris-versicolor":
		y[i][1] = 1.0
	else:
		y[i][2] = 1.0

#split training and test data
X_train = X[:120]
X_test = X[120:]
y_train = y[:120]
y_test = y[120:]


# train NN 10000 iterations
NN = Neural_Network()
for i in range(10000):
	# print("# " + str(i) + "\n")
	# print("Input (scaled): \n" + str(X))
	# print("Actual Output: \n" + str(y))
	# print("Predicted Output: \n" + str(NN.forward(X)))
	# print("Loss: \n" + str(np.mean(np.square(y - NN.forward(X))))) # mean sum squared loss
	# print("\n")
	NN.train(X_train, y_train)

# NN.predict()
print(NN.accuracy(X_test, y_test))



