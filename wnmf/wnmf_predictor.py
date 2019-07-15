# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 14:03:52 2019

@author: jonathan
"""

import numpy as np
import pandas as pd
import math
import sys
sys.path.insert(0, '../')

def get_index_dicts(training_um_df):
    user_indices = training_um_df.index.to_numpy()
    user_indices = [int(x) for x in user_indices]
    print(user_indices)
    item_indices = training_um_df.columns.to_numpy()
    item_indices = [int(x) for x in item_indices]
    print(item_indices)
    #need to make dictionary such that keys are actual IDs, and values are positional.
    uid_to_index = {} #actual user id -> zero-based index in 2d array
    for i in range(len(user_indices)):
        uid_to_index[user_indices[i]] = i

    iid_to_index = {} #actual item id -> zero-based index in 2d array
    for i in range(len(item_indices)):
        iid_to_index[item_indices[i]] = i

    return uid_to_index, iid_to_index
#takes: a U factor resulting from WNMF of a training set utility matrix; a V factor resulting from WNMF of a training set utlity 
def predict(training_um_df, training_u_df, training_v_df, test_og_df, users_and_items, dest_filename):
    u = training_u_df.to_numpy()
    v = training_v_df.to_numpy()
    print(u)
    print(v)
    #rebuild prediction matrix by multiplying factor matrices
    pm = np.matmul(u, v)
    uid_to_index, iid_to_index = get_index_dicts(training_um_df)
    
    users_and_items = users_and_items.to_numpy()
    predictions = np.zeros(len(users_and_items), dtype=float)
    results = test_og_df
    
    for i in range(len(users_and_items)):
        print('Predicting user/item pair ' + str(i + 1))
        
        user = users_and_items[i][0]
        item = users_and_items[i][1]
        if user not in uid_to_index:
            prediction = math.nan
        elif item not in iid_to_index:
            prediction = math.nan
        else:
            prediction = pm[uid_to_index[user]][iid_to_index[item]]
            if prediction > 5:
                prediction = 5
            elif prediction < 1:
                prediction = 1
        print("User: " + str(user) + " Item: " + str(item) + " Prediction: " + str(prediction))
        predictions[i] = prediction
    
    predictions = pd.Series(predictions)
    
    results['prediction'] = predictions
    print(results)
    results.to_csv(dest_filename)
    return results
    
    
def main():
    #get test_og and users/items df
    users_and_items = pd.read_csv('../datasets/ml-100k/u1.test', sep='\t', header=None)
    users_and_items.columns = ['user', 'item', 'observed', 'timestamp']
    del users_and_items['timestamp']
    test_og_df = pd.DataFrame.copy(users_and_items)
    del users_and_items['observed']
    
    training_um_df = pd.read_csv('../datasets/ml-100k/utility-matrix/ml_u1_item_um.csv', index_col = 0)
    print(training_um_df)
    
    import ml_prediction_matrix_builder as mlpmb
    u_df, v_df = mlpmb.build(training_um_df, 'wnmf_predictor_test_')
    '''
    u_df = pd.read_csv('wnmf_test_u_matrix.csv', index_col = 0)
    v_df = pd.read_csv('wnmf_test_v_matrix.csv', index_col = 0)
    '''
    predictions_df = predict(training_um_df, u_df, v_df, test_og_df, users_and_items, 'wnmf_first_test_results.csv')
    
    
    from item_similarity import prediction_error_mae as mae
    print("MAE: ")
    mae.calculate_mae(predictions_df)
    

if __name__ == '__main__':
    main()
    
    