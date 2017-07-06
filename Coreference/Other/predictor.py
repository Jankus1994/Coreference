# Jan Faryad
# 23. 6. 2017

from sklearn.neighbors import KNeighborsClassifier
import os
import joblib
import sys

class Predictor:
    def predict( self, model_name):
        #( feature_vectors, spam, id_vectors ) = self.read_input()
        ( feature_vectors, id_vectors ) = self.read_input()
        predictor = joblib.load( model_name)
        results = list( predictor.predict( feature_vectors))
        #print( len( [a for a in results if a == True ]))
        #self.process_results( id_vectors, spam, results)
        self.process_results( id_vectors, results)
        
    def read_input( self):
        feature_vectors = []
        id_vectors = []
        target_vector = []
        for line in sys.stdin:
            fields = line.split( '\t')
            
            feature_vector = []
            for field in fields[:-6]: # features
                feature_vector.append( self.string_to_bool( field))
            feature_vectors.append( feature_vector)
            
            #spam = fields[-6:-4]
            
            id_vector = []
            for field in fields[-4:]: # ids
                id_vector.append( int( field))  
            id_vectors.append( id_vector)
            
        #return  ( feature_vectors, spam, id_vectors )
        return  ( feature_vectors, id_vectors )
                 
    def string_to_bool( self, string):
        if ( string == "True"):
            return True
        return False
    
    #def process_results( self, id_vectors, spam, results):
    def process_results( self, id_vectors, results):
        if ( len( id_vectors) != len( results) ):
            return        
        for i in range( len( results)):
            id_vector = id_vectors[i]
            result = results[i]
            #pronoun_id = ( id_vector[0], id_vector[1] )
            #antecedent_id = ( id_vector[2], id_vector[3] )
            if ( result ):
                for id in id_vector:
                    print( id, end='\t')
                #print( spam, str( result))
                print( str( result))
        
if ( len( sys.argv) == 2 ):
    p = Predictor()
    p.predict( sys.argv[1])

    
        
        
