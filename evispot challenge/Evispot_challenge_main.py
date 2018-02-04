"""
    This is my code to solve the evispot challenge. The code employs the network3.py file from the
    repository https://github.com/MichalDanielDobrzanski/DeepLearningPython35 which implements the
    code from https://github.com/mnielsen/neural-networks-and-deep-learning for python 3.5.

    The basis for this appraoch is a 3 layer neural network trained via stochastic gradient descent
    as described in Nielsen's book under http://neuralnetworksanddeeplearning.com/ .
"""

# First we load the addionally needed libraries

import numpy as np
import pandas as pd # pandas is used for loading and transforming data
from datetime import datetime as dt
from collections import Counter

# Load the data from csv file. df is for data frame, a R and pandas class

training_data = pd.read_csv('C:\\Users\\Becks\\Desktop\\training_test.csv', low_memory=False)
test_data = pd.read_csv('C:\\Users\\Becks\\Desktop\\test_test.csv', low_memory=False)
#training_data = pd.read_csv('C:\\Users\\Becks\\Desktop\\training_data.csv')
#test_data = pd.read_csv('C:\\Users\\Becks\\Desktop\\test_data.csv')

"""
    Start data cleaning, i.e. fill empty cells, convert string variables into
    binary numerics via pivot table, merge low sum columns (for city, country),
    cut unnecessary cells
    Do it for both training and test data to make sure both are equally prepared
"""

# Keeping only data that is needed as input
training_data = training_data [['BIRTH_YEAR', 'DATE', 'TRANS_AMO', 'MRCH_CITY', 'MRCH_CTRY', 'SEX', 'TRANSTYP_CODE']]

# Create the clean input data as an empty list to which the arrays of data are added consequently
c_training = []
c_test = []

# Create variable for the amount of rows of training data
n_rows, ncols = training_data.shape
print(n_rows, ncols)

# For all columns, extract the data that is needed and then append it to the clean input list
for i in training_data.keys():

    # Check whether feature is in both data sets, if not skip, else continue with loop execution for the feature
    if i not in test_data.keys():
        print('Error: Missing features in test data!')
        continue
    
    else:
        # Convert column to list    
        temp = training_data[i].values
        temp_test = test_data[i].values

    # If the data is numeric, just convert to numeric
    if i in ['BIRTH_YEAR','TRANS_AMO']:
        temp = [str(s).replace(' ','NaN').replace(',','.') for s in temp]
        temp = np.array(temp).astype(np.float)
        
        temp_test = [str(s).replace(' ','NaN').replace(',','.') for s in temp_test]
        temp_test = np.array(temp_test).astype(np.float)

        """
        # Replace missing data with the mean of the non-missing data, this will lead to 0s after normalising as it cannot change the mean
        temp [np.where(np.isnan(temp))] = np.nanmean(temp)

        This could affect the standard deviation, leave nan for now.
        """
    
        # Append data to the input data
        c_training.append(temp)
        c_test.append(temp_test)

    # Now for the date split
    elif i in ['DATE']:
        
        # First extract day of the month
        dom = np.array([int(s.split('/')[1]) for s in temp])
        c_training.append(dom)
        
        dom = np.array([int(s.split('/')[1]) for s in temp_test])
        c_test.append(dom)

        # Now extract month
        month = np.array([int(s.split('/')[0]) for s in temp])
        c_training.append(month)
        
        month = np.array([int(s.split('/')[0]) for s in temp_test])
        c_test.append(month)

        # Now get weekday (as integer 0 for monday to 6 for sunday)
        wd = np.array([dt.strptime(s, '%m/%d/%Y').weekday() for s in temp])
        c_training.append(wd)
        
        wd = np.array([dt.strptime(s, '%m/%d/%Y').weekday() for s in temp_test])
        c_test.append(wd)

        # Finally convert the date to an epoch integer
        temp = np.array([dt.strptime(s, '%m/%d/%Y').timestamp() for s in temp])
        c_training.append(temp)
        
        temp_test = np.array([dt.strptime(s, '%m/%d/%Y').timestamp() for s in temp_test])
        c_test.append(temp_test)

    # Next will be the sex and trans_code categories, where all are needed but empty categories will not be added
    elif i in ['SEX', 'TRANSTYP_CODE']:
        
        # Get unique categories, taken only from training set as unknown categories from test set cannot be trained through the model
        unique_cat = np.unique(temp).tolist()

        # Drop empty categories
        if ' ' in unique_cat:
            unique_cat.remove(' ')

        # For all unique categories, add a vector that is 1 if an event belongs to the category or 0 otherwise
        for uc in unique_cat:
            c_training.append(np.array([int(x == uc) for x in temp]))
            c_test.append(np.array([int(x == uc) for x in temp_test]))

    # Finally will be the category columns that need to be split into multiple binary columns but cannot use every possible category
    else:
        # Count how often each categoy occurs, taken only from training set as unknown categories from test set cannot be trained through the model
        count = Counter(temp)
        # Select only the most important categories, in this case all on or above the 80th percentile
        imp_cat = [x for x,y in count.items() if y >= np.percentile(list(count.values()),80)]

        # For all important categories, add a vector that is 1 if an event belongs to the category or 0 otherwise
        for ic in imp_cat:
            c_training.append(np.array([int(x == ic) for x in temp]))
            c_test.append(np.array([int(x == ic) for x in temp_test]))

        # Summarise all other categories in one 'other' category
        c_training.append(np.array([int(x not in imp_cat) for x in temp]))
        c_test.append(np.array([int(x not in imp_cat) for x in temp_test]))


#print(c_training)

"""
import network3 # this includes the neural network class
from network3 import Network, ConvPoolLayer, FullyConnectedLayer, SoftmaxLayer # This masks the classes from network3.py to be used without prefix

# read data:
training_data, validation_data, test_data = network3.load_data_shared()
# mini-batch size:
mini_batch_size = 10

net = Network([
    FullyConnectedLayer(n_in=784, n_out=100),
    SoftmaxLayer(n_in=100, n_out=10)], mini_batch_size)
net.SGD(training_data, 60, mini_batch_size, 0.1, validation_data, test_data)
"""
