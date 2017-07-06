# Jan Faryad
# 21. 6. 2017
#
# main programm that roofs machine learning of coreference from gold data in CoNLL-U format, runs prediction and evaluation
from udapi.core.block import Block

from conll_processor import CoNLL_processor
from conll_selector import CoNLL_selector
from conll_api import CoNLL_API as api
from conll_add_coref import CoNLL_add_coreference
from conll_evaluator import CoNLL_evaluator

from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
import os

path = "C:\Komodo\Projekty\\"

class Conll_main( Block):
    def process_document( self, document):
        
        
    

# for these files is necessary to run previous parts of project (conversion from PDT to plain text, UDPipe for conversion to CoNLLU
# and transfer of coreference information from PDT to CoNLL-U)
# name of the file
file_1 = "cmpr9410_001" # train 1
file_2 = "lnd94103_052" # train 8
file_3 = "ln94206_32" # train 5
file_4 = "cmpr9410_032" # train 2
file_5 = "ln94204_7" # train 2
file_6 = "mf930713_046" # train 2
file_7 = "ln94210_105" # train 2
file_8 = "ln95048_134" # train 3
file_9 = "mf920922_131" # train 7
file_10 = "mf930713_085" # train 1
file_11 = "mf930713_118" # train 3
file_12 = "ln95048_117" # train 6

list_of_files = [ file_1, file_2, file_3, file_4, file_5, file_6, file_7, file_8, file_9, file_10, file_11, file_12 ]
precision_sum = 0 # observed properties of recognition - will be used for evaluation
recall_sum = 0    #
for file in list_of_files: # cross validation, one file will be considered as testing file, the others as traning files
    train = [ f for f in list_of_files if f != file ] 
    test = file

    feature_vectors = []
    target_values = []
    
    for name in train: # building feature vectors from training files
        input = open( path + name + ".out.conll", 'r', encoding="utf8") # file with coreference information
        proc = CoNLL_processor( input)     # processing the document
        document = proc.process_document() #        
        input.close()
        
        selec = CoNLL_selector( document)  # selecting of feature vectors with target values for training
        vectors = selec.process_document() #
    
        for i in vectors:
            # vectors have form ( Node - pronoun, Node - candidate for coreference, feature vector, target bool value (are these two nodes coreferents?) )
            feature_vectors.append( i[2])
            target_values.append( i[3])

    # clf = svm.SVC(gamma=0.001, C=100.) # didn't work... ?
    knn = KNeighborsClassifier() # knn works much better
    #knn = svm.SVC(gamma=0.001, C=100.)
    knn.fit( feature_vectors, target_values) # MACHINE LEARNING
    #
    input = open( path + test + ".out.conll", 'r', encoding="utf8") # testing file with coreference information    
    proc = CoNLL_processor( input)     # processing document    
    document = proc.process_document() #
    input.close()
    
    selec = CoNLL_selector( document)  # selecting of feature vectors with target values for evaluation
    vectors = selec.process_document() #
    
    feature_vectors = []              # similar as for training files
    target_values = []                # 
    for i in vectors:                 #
        feature_vectors.append( i[2]) #
        target_values.append( i[3])   #
        
    results = list( knn.predict(feature_vectors)) # PREDICTION
    print( results.count(True), target_values.count(True))
    coreference_triplets = [] # triplets ( pronound id, candidate id, bool value - are they coreferents? )
    for i in range( len( vectors)):
        pronoun_id = api.get_full_id( vectors[i][0])
        referent_id = api.get_full_id( vectors[i][1])
        triplet = ( pronoun_id, referent_id, bool(results[i]) )
        coreference_triplets.append( triplet)
        
    input = open( path + test + ".outp.conll", 'r', encoding="utf8") # test files WITHOUT coreference information
    output = open( path + test + ".test.conll", 'w', encoding="utf8") # adding detected coreference
    coref_adder = CoNLL_add_coreference( input, output)               #
    coref_adder.add_coreference( coreference_triplets)                #
    input.close()
    output.close()
    
    # EVALUATION - comparing of manually (gold) and automatically marked coreference
    gold_input = open( path + test + ".out.conll", 'r', encoding="utf8") # test file with coreference
    auto_input = output = open( path + test + ".test.conll", 'r', encoding="utf8") # output of adder - previous step
    evaluator = CoNLL_evaluator( gold_input, auto_input) # evaluating
    ( precision, recall ) = evaluator.evaluate()         #
    
    precision_sum += precision
    recall_sum += recall
    print(precision, recall)
    print('\n')
    

# average precision and recall
print( "Average precision: ", precision_sum / len( list_of_files))
print( "Average recall: ", recall_sum / len( list_of_files))
#print( "Average precision: ", precision_sum )
#print( "Average recall: ", recall_sum )
