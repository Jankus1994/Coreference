# Jan Faryad
# 4. 7. 2017

from sklearn import neighbors, tree, svm, linear_model
import joblib
import sys

class Trainer():
    def train( self, model_name, file_name):
        self.inputfile = open( file_name, 'r')
        ( feature_vectors, target_vector ) = self.read_input()
        self.inputfile.close()
        
        # which machine learning method we use:
        
        #model = neighbors.KNeighborsClassifier()        
        model = tree.DecisionTreeClassifier()
        #model = linear_model.LinearRegression()
        #model = linear_model.LogisticRegression()
        #model = linear_model.Perceptron()
        #model = svm.SVC()
        
        model.fit( feature_vectors, target_vector )        
        joblib.dump( model, model_name) # saving the model into a file with the given name
        
    def read_input( self):
        """ reading feature vectors from the given input file """
        NONTRAINING_VALUES_NUMBER = 7 # the last value in the row aren't for training:
                                    #target value, pronoun form, candidate form, pronoun id (sent / worrd), candidate id (sent, word)
        feature_vectors = []
        target_vector = []
        for line in self.inputfile:
            fields = line.split( '\t')
            feature_vector = []            
            for field in fields[ : -NONTRAINING_VALUES_NUMBER ]: # only values for training
                feature_vector.append( self.convert( field))
            feature_vectors.append( feature_vector)         
            target_vector.append( self.convert( fields[ -NONTRAINING_VALUES_NUMBER ]))
            # the resto of values is omitted - the ids are important for adding the predicted information to CoNLL-U, forms are only for better orientation in the data
        return  ( feature_vectors, target_vector )
    
    def convert( self, string):
        try:
            number = int( string) # integer value
            return number
        except:
            if ( string == "True" ):
                return True
            return False                               
        
if ( len( sys.argv) == 3 ):
    t = Trainer()
    t.train( sys.argv[1], sys.argv[2])

