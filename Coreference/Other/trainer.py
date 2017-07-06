# Jan Faryad
# 4. 7. 2017

from sklearn.neighbors import KNeighborsClassifier
import os
import joblib
import sys

class Trainer:
    def train( self, model_name):
        ( feature_vectors, target_vector ) = self.read_input()
        knn = KNeighborsClassifier()
        knn.fit( feature_vectors, target_vector )
        joblib.dump(knn, model_name)
        #mvv = joblib.load( model_name)
        #results = list( knn.predict( feature_vectors))
        #print(len([a for a in range(len(results)) if (results[a] == True and target_vector[a] == True ) ] ) )
        #print( results[:10] == target_vector[:10] )
        
    def read_input( self):
        feature_vectors = []
        target_vector = []
        for line in sys.stdin:
            fields = line.split( '\t')
            feature_vector = []
            for field in fields[:-7]:
                feature_vector.append( self.string_to_bool( field))
            feature_vectors.append( feature_vector)
            target_vector.append( self.string_to_bool( fields[-7]))
        return  ( feature_vectors, target_vector )
    
    def string_to_bool( self, string):
        if ( string == "True"):
            return True
        return False
                                
        
if ( len( sys.argv) == 2 ):
    t = Trainer()
    t.train( sys.argv[1])

