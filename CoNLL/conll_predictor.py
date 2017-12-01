# Jan Faryad
# 11. 10. 2017

from sklearn.neighbors import KNeighborsClassifier
import os
import joblib
 
class Conll_predictor():   
    def predict( self, vectors, model_name):        
        ( feature_vectors, id_vectors ) = self.read_vectors( vectors)               
        predictor = joblib.load( model_name)
        #for p in vectors:
        #    print( p)
        results = list( predictor.predict( feature_vectors))
        #print( True in results)

        if ( len( id_vectors) == len( results) ):
            recognized = [ id_vectors[i] for i in range( len( results)) if results[i] ]  
            return recognized
        
    def read_vectors( self, vectors):
        feature_vectors = []
        id_vectors = []
        for vector in vectors:
            feature_vector = vector[:-6]
            feature_vectors.append( feature_vector)
            
            id_vector = vector[-4:]
            id_vectors.append( id_vector)

        return  ( feature_vectors, id_vectors )
