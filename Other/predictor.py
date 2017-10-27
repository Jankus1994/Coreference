# Jan Faryad
# 11. 10. 2017

from udapi.core.block import Block
import sys
from sklearn.neighbors import KNeighborsClassifier
import os
import joblib
import sys

class Predictor( Block):   
    def process_document( self, doc):        
        model_name = "cz_model"
        file_name = "vectors.txt"
        self.inputfile = open( file_name, 'r')  
        #self.kontrola = open("kontrola.txt", 'a')
        ( feature_vectors, id_vectors ) = self.read_input()               
        self.inputfile.close()
        predictor = joblib.load( model_name)
        results = list( predictor.predict( feature_vectors))
        #print( len( [a for a in results if a == True ]))
        #self.process_results( id_vectors, spam, results)
        result_name = "results.txt"
        self.outputfile = open( result_name, 'w')  
        self.process_results( id_vectors, results)   
        self.outputfile.close()
        
    def read_input( self):
        feature_vectors = []
        id_vectors = []
        target_vector = []
        for line in self.inputfile:
            fields = line.split( '\t')
            #self.kontrola.write( line + '\n')
            feature_vector = []
            for field in fields[:-6]: # features
                feature_vector.append( self.convert( field))
            feature_vectors.append( feature_vector)
            
            #spam = fields[-6:-4]
            
            id_vector = []
            for field in fields[-4:]: # ids
                id_vector.append( int( field))  
            id_vectors.append( id_vector)
            
        #return  ( feature_vectors, spam, id_vectors )
        return  ( feature_vectors, id_vectors )
                 
    def convert( self, string):
        try:
            number = int( string)
            return number
        except:
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
                    self.outputfile.write( str( id) + '\t')
                self.outputfile.write('\n')
        
if ( len( sys.argv) == 3 ):
    p = Predictor()
    p.predict( sys.argv[1], sys.argv[2])

    
        
        
