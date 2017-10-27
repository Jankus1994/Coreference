# Jan Faryad
# 4. 7. 2017

from sklearn.neighbors import KNeighborsClassifier
import os
import joblib
import sys

class Trainer():
    def train( self, model_name, file_name):
        self.inputfile = open( file_name, 'r')
        ( feature_vectors, target_vector ) = self.read_input()
        self.inputfile.close()
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
        for line in self.inputfile:
            fields = line.split( '\t')
            feature_vector = []
            for field in fields[:-7]:
                feature_vector.append( self.convert( field))
            feature_vectors.append( feature_vector)
            target_vector.append( self.convert( fields[-7]))
        return  ( feature_vectors, target_vector )
    
    def convert( self, string):
        try:
            number = int( string)
            return number
        except:
            if ( string == "True"):
                return True
            return False
                                
        
if ( len( sys.argv) == 3 ):
    t = Trainer()
    t.train( sys.argv[1], sys.argv[2])

