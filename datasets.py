# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 18:38:50 2019

@author: jonathan
"""

'''
Dataset Class
I created this class because each dataset can be represented as an object.
Each dataset has a source csv file,
and will have a utility matrix, a similarity matrix, and a 
Objects are an easy way to bundle them together.
'''

import pandas as pd
from item_similarity import item_predictor
import json
import sys
sys.path.insert(0, 'datasets/yelp_dataset/utility-matrix/')

class Dataset:
    #INSTANCE VARIABLES
    #text description of dataset
    name = None
    
    #dataframe processed directly from original data file
    og_df = None
    
    #utility matrix dataframe
    um_df = None
    
    #similarity matrix dataframe
    sm_df = None    
    
    
    #CONSTRUCTOR
    #og - original data; um - utility matrix; sm - similarity matrix
    #Keyword Arguments: data=ml,yelp; algo=item,user,wnmf; sim=pearson,cosine,wnmf
    def __init__(self, name, og_file, um_file, sm_file, data='ml', algo='item', sim='pearson'):
        self.name = name
        print(name + ' is being prepared...')
        if data == 'ml':
            self.og_df = self.build_ml_og_df(og_file) #function returns df
            if algo == 'item':
                self.um_df = self.build_ml_item_um(um_file) #function returns um df
            elif algo == 'user':
                self.um_df = self.build_ml_user_um(um_file) #function returns um df
            elif algo == 'wnmf':
                self.um_df = self.build_ml_wnmf_um(um_file)
            if sim == 'pearson':
                    self.sm_df = self.build_ml_pearson_sm(sm_file) #function returns sim df
            elif sim == 'cosine':
                    self.sm_df = self.build_ml_cosine_sm(sm_file)
        if data == 'yelp':
            self.og_df = self.build_yelp_og_df(og_file, 
                                               data='yelp') #function returns df
            if algo == 'item':
                self.um_df = self.build_yelp_item_um(um_file) #function returns um df
            elif algo == 'user':
                self.um_df = self.build_yelp_user_um(um_file) #function returns um df
            elif algo == 'wnmf':
                self.um_df = self.build_yelp_wnmf_um(um_file)
            if sim == 'pearson':
                    self.sm_df = self.build_yelp_pearson_sm(sm_file) #function returns sim df
            elif sim == 'cosine':
                    self.sm_df = self.build_yelp_cosine_sm(sm_file)
        
        
        
    #METHODS
    
    #build a dataframe from the source csv file #GOOD 6/25
    def build_ml_og_df(self, og_file):
        try:
            og_df = pd.read_csv(og_file, sep='\t', names=['user', 'movie', 'rating', 'timestamp'])
            del og_df['timestamp']
            print("Original MovieLens data file ready (og_df)")
            return og_df
        except FileNotFoundError:
            print("build_ml_og_df error: Original data file not at location given")    
            
    #ITEM-BASED METHODS
    
    #builds item-based utility matrix for data file at specified filename #GOOD 6/25
    #results in an item-based utility matrix with columns denoted '1', '2', '3' (strings) and rows 1, 2, 3 (integers)
    def build_ml_item_um(self, um_file):
        um_df = None
        try:
            um_df = pd.read_csv(um_file, index_col = 0)
        except FileNotFoundError:
            print('Building MovieLens item-based utility matrix for the \'' + self.name + '\' dataset')
            from item_similarity import ml_item_um_builder
            um_df = ml_item_um_builder.build(self.og_df, um_file)
        print('MovieLens item-based utility matrix ready (um_df)')
        #print(um_df)
        return um_df
            
        '''
        #SHOULD CALL ml_utility_builder.build('csv', type='item') #item or user-based, depending on type argument
        #import item_utility_builder
        #item_utility_builder.build(params)
        #always has to specify a source file
        #   tries to read source file
        #       if fails, builds source file from previous step dataframe
        #           if no previous step dataframe, throws error
        #   returns dataframe
        
        #if no source file for the dataset has been specified:
        if self.item_utility_source is None:
            if self.og_df is None:
                self.build_ml_og_df()
            self.item_utility_df = self.og_df.pivot_table(index='user', columns='movie', values='rating')
            #print(self.item_utility_df)
            self.item_utility_df.to_csv(dest_filename)
            self.item_utility_source = dest_filename
        elif self.item_utility_df is None:
            self.build_ml_item_um_df()
        '''
    '''
    def build_ml_item_um_df(self):
        if self.item_utility_source is None:
            print('build_item_utility_df Error: build a utility matrix source csv file first')
        else:
            self.item_utility_df = pd.read_csv(self.item_utility_source, index_col = 0)
    '''
    
    '''
    #build item-based similarity matrix using Pandas Corrwith function (test purposes only)
    def build_item_pearson_sim_corrwith(self, dest_filename):
        #NEED TO IMPLEMENT CODE THAT MAKES IT WORK EVEN IF UTILITY NOT BUILT, etc.
        
        #if utility matrix not built yet
        if self.item_utility_df is None:
            print('build_item_pearson_sim Error: Utility matrix must be built first')
            
        else:            
            #create first column/dataframe
            row = self.item_utility_df.corrwith(self.item_utility_df['1']) #may need to make string
            similarity = pd.DataFrame(row, columns=[1]) #may need to make string
            
            for i in range(2, len(self.item_utility_df.columns)):
                if i % 10 == 0:
                    print('Correlating item ' + str(i) + '...')
                similarity[i] = self.item_utility_df.corrwith(self.item_utility_df[str(i)])
            print(similarity)
            self.item_pearson_sim_df = similarity
            similarity.to_csv(dest_filename)
            self.item_pearson_sim_source = dest_filename
        '''
            
    def build_ml_pearson_sm(self, sm_file):
        sm_df = None
        try:
            sm_df = pd.read_csv(sm_file, index_col = 0)
        except FileNotFoundError:
            print('Building MovieLens Pearson correlation similarity matrix for the \'' + self.name + '\' dataset')
            import ml_pearson_sm_builder
            sm_df = ml_pearson_sm_builder.build(self.um_df, sm_file)
        print('MovieLens Pearson correlation-based similarity matrix ready (sm_df)')
        return sm_df
    
    def build_ml_cosine_sm(self, sm_file):
        sm_df = None
        try:
            sm_df = pd.read_csv(sm_file, index_col = 0)
        except FileNotFoundError:
            print('Building MovieLens cosine similarity matrix for the \'' + self.name + '\' dataset')
            import ml_cosine_sm_builder
            sm_df = ml_cosine_sm_builder.build(self.um_df, sm_file)
        print('MovieLens cosine similarity matrix ready (sm_df)')
        #print(sm_df)
        return sm_df
    
            
    '''
    def build_user_pearson_sim(self, dest_filename):     
        #if utility matrix not built yet
        if self.item_utility_df is None:
            print('build_item_pearson_sim Error: Utility matrix must be built first')           
        else:
            self.user_utility_df = self.item_utility_df.transpose()
            utility_np = self.user_utility_df.to_numpy()
            similarity_np = np.zeros((len(utility_np[0]), len(utility_np[0])), dtype=float) 
            #ITERATE OVER DATA
            for i in range(len(similarity_np)):
                print("User " + str(i))
                for j in range(len(similarity_np[i])):
                    if similarity_np[j][i] != 0:
                        similarity_np[i][j] = similarity_np[j][i]
                    else:
                        similarity_np[i][j] = pearson_corr(utility_np[:, i], utility_np[:, j])
            
            #EXPORT COMPLETED SIMILARITY MATRIX
            similarity = pd.DataFrame(similarity_np, index = self.user_utility_df.columns, columns = self.user_utility_df.columns)
            similarity.to_csv(dest_filename)
            self.user_pearson_sim_source = dest_filename
            self.user_pearson_sim_df = similarity
            
            print("User-Based Pearson")
            print(similarity)
            
    def build_user_pearson_sim_df(self):
        if self.user_pearson_sim_source is None:
            print('build_user_pearson_sim_df Error: build a user-based Pearson correlation source csv file first with build_user_pearson_sim')
        else:
            self.user_pearson_sim_df = pd.read_csv(self.user_pearson_sim_source, index_col = 0)
    '''

    #USER-BASED METHODS
    def build_ml_user_um(self, um_file):
        um_df = None
        try:
            um_df = pd.read_csv(um_file, index_col = 0)
        except FileNotFoundError:
            print('Building MovieLens user-based utility matrix for the \'' + self.name + '\' dataset')
            from user_similarity import ml_user_um_builder
            um_df = ml_user_um_builder.build(self.og_df, um_file)
        print('MovieLens user-based utility matrix ready')
        return um_df
    '''
    #NEED TO FINISH THIS
    #YELP USER UM function called here needs to return a dictionary
    def build_yelp_user_um(self, um_file):
        um_df = None #though it's called um_df, it's a dictionary
        try:
            with open(um_file, 'r') as f:
                um_df = json.load(f)
        except FileNotFoundError:
            print('Building Yelp user-based utility matrix for the \'' + self.name + '\' dataset')
            import yelp_utility_matrix_builder_user
    '''
            
            
    
    def build_yelp_cosine_sm(self, sm_file):
        sm_df = None
        try:
            with open(sm_file, 'r') as f:
                sm_df = json.load(f)
        except FileNotFoundError:
            import yelp_cosine_sm_builder
            print('Building Yelp cosine similarity matrix for the \'' + self.name + '\' dataset') 
            sm_df = yelp_cosine_sm_builder.build(self.um_df, sm_file)
        return sm_df

#Class for training/test set pairs
#TestSet subclass inherits from Dataset superclass
class TestSet(Dataset):
    user_item_pairs_df = None
    predictions_df = None
    error_df = None

    def build_ml_og_df(self, og_file):
        try:
            og_df = pd.read_csv(og_file, sep='\t', header=None)
            og_df.columns = ['user', 'item', 'observed', 'timestamp']
            del og_df['timestamp']
            print("Original MovieLens test set file ready (test.og_df)")
            return og_df
        except FileNotFoundError:
            print("TestSet.build_ml_og_df error: Original test set file not at location given") 
    
    def build_user_item_pairs_df(self, og_file):
        try:
            df = pd.read_csv(og_file, sep='\t', header=None)
            df.columns = ['user', 'item', 'observed', 'timestamp']
            del df['observed']
            del df['timestamp']
            print("MovieLens test user-item pairs ready (test.user_item_pairs_df)")
            return df
        except FileNotFoundError:
            print("TestSet.build_ml_og_df error: Original test set file not at location given when trying to build user_item_pairs_df") 
    
    
    #NON-CONSTRUCTOR-BASED METHODS
    #takes a CSV
    #conventions do not apply to this
    def build_predictions_df(self, csv=None, predictions=None):
        predictions_df = None
        if csv is not None:
            predictions_df = pd.read_csv(csv, index_col=0)
            predictions_df['observed'] = self.og_df['observed']
            print('Prediction results from test set loaded from file (test.predictions_df)')
        elif predictions is not None:
            predictions_df = self.og_df
            predictions_df['prediction'] = predictions
            print('Prediction results ready (test.predictions_df)')
        else:
            print('No prediction file loaded; currently, predictions_df = None')
        return predictions_df
            
    
    def build_error_df(self):
        self.error_df = pd.DataFrame(self.predictions_df)
        self.predictions_df['error'] = (self.predictions_df['observed rating'] - self.predictions_df['prediction']).abs()
    
    def save_test_results(self, dest_filename):
        self.predictions_df.to_csv(dest_filename)
    
    #TestSet CONSTRUCTOR
    def __init__(self, name, og_file, data="ml", prediction_file=None):
        self.name = name
        print(name + ' is being prepared...')
        if data == "ml":
            self.og_df = self.build_ml_og_df(og_file)
        elif data == "yelp":
            self.og_df = self.build_yelp_og_df(og_file)
        self.user_item_pairs_df = self.build_user_item_pairs_df(og_file)
        if prediction_file is not None:
            self.predictions_df = self.build_predictions_df(csv=prediction_file)

#this class is to bundle together a training set and a test set
class TrainingAndTest:
    name = None
    algorithm = None
    training = None
    test = None
    
    #CONSTRUCTOR
    def __init__(self, name, ):
        self.name = name
        print("Temporary fix: Please initialize the .training and .test objects using their own constructors")
        '''
        self.training = Dataset(self.name + ' training set')
        self.test = TestSet(self.name + ' test set')
        '''
    '''
    def __init__(self, training_source, test_source, training_um, training_sm, ):
        self.training = Dataset(self.name + ' training set')
        self.test = TestSet(self.name + ' test set')
    '''
        
    
#CORRELATION/DISTANCE FUNCTIONS    
   
#DATASET LOADING FUNCTIONS
#format: load_<dataset name>

#load MovieLens datasets
        
    #MovieLens 100k main source file
def load_ml_100k():
    ml_100k = Dataset("MovieLens 100k main file")
    ml_100k.algorithm = 'neighborhood-based collaborative filtering'
    ml_100k.source = 'datasets/ml-100k/u.data'
    ml_100k.build_ml_og_df() #build dataframe from the source
    ml_100k.item_utility_source = 'datasets/ml-100k/utility-matrix/ml_100k_item_utility.csv'
    #ml_100k.build_item_utility('datasets/ml-100k/utility-matrix/ml_100k_item_utility.csv') #build item-based utility matrix dataframe
    ml_100k.build_item_utility_df()
    ml_100k.item_pearson_sim_source = 'item_similarity/ml_100k_item_pearson_sim.csv'
    #ml_100k.build_item_pearson_sim('item_similarity/ml_100k_item_pearson_sim.csv')
    ml_100k.build_item_pearson_sim_df() #build item-based utility matrix dataframe
    #returns Dataset object to calling function
    return ml_100k


    #MovieLens 100k u1 test/training set
def load_ml_u1():
    #NEED ONLY FUNCTIONS TO BE BUILD FUNCTIONS THAT TAKE A CSV
    ml_u1 = TrainingAndTest('MovieLens u1 training/test sets')
    ml_u1.training = Dataset(
        'u1 training set',                                          #name
        'datasets/ml-100k/u1.base',                                 #original source
        'datasets/ml-100k/utility-matrix/ml_u1_item_utility.csv',   #utility matrix
        'item_similarity/ml_u1_item_cosine_sim.csv', sim='cosine') #similarity matrix
    ml_u1.test = TestSet(
        'u1 test set',                                              #name
        'datasets/ml-100k/u1.test', prediction_file='item_similarity/ml_u1_2019_06_24_test_results.csv') #test results
    return ml_u1
    
def load_yelp_stut():
    yelp_stut = Dataset("Yelp Stuttgart, Germany Reviews")
    yelp_stut.item_utility_source = 'datasets/yelp_dataset/utility-matrix/yelp_utility_matrix_stuttgart.csv'
    yelp_stut.build_item_utility_df()
    yelp_stut.item_pearson_sim_source = 'item_similarity/yelp_stut_item_pearson_sim.csv'
    yelp_stut.build_user_pearson_sim('user_similarity/yelp_stut_user_pearson_sim.csv')
    print(yelp_stut.user_pearson_sim_df)
    
def main():
    ml_u1 = load_ml_u1()
    print(ml_u1.test.predictions_df)

if __name__ == '__main__':
    main()
    
        
        
        



