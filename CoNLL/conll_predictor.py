# Jan Faryad
# 11. 10. 2017

""" class for predicting corefeernce with a given model and feature vectors """

from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
import os
import joblib
 
class Conll_predictor():   
    def predict( self, vectors, model_name):
        """ main method for prediction """
        ( feature_vectors, id_vectors ) = self.read_vectors( vectors)
        predictor = joblib.load( model_name)
        results = list( predictor.predict( feature_vectors))

        if ( len( id_vectors) == len( results) ):
            # we return ids of pairs, whose coerferenmce was detected
            recognized = [ id_vectors[i] + [ results[i] ] for  i in range( len( results)) if results[i] ]#> 0.07 ]   
            return recognized
        
    def read_vectors( self, vectors): # -> pair ( feature vectors : list of lists of features - ints/bools, id vectors : list of lists of ints )
        """ processing the given vectors - exctracting the features for the model, the ids, but ignoring the word forms"""
        feature_vectors = []
        id_vectors = []
        for vector in vectors:
            feature_vector = vector[:-6] # all featuers except thw word forms (2x) and IDs
            feature_vectors.append( feature_vector)
            
            id_vector = vector[-4:] # IDs ( pronoun senttence id, pronoun word id, candidate sentence id, candidate word id, 
            id_vectors.append( id_vector)

        return  ( feature_vectors, id_vectors )
