# Jan Faryad
# 10. 3. 2018

""" main class (as udapi block) for prediction usecase """

from udapi.core.block import Block
from udapi.block.demo.Coreference.CoNLL.conll_specific_selectors import Conll_rel_prediction_selector, Conll_dem_prediction_selector, Conll_prs_prediction_selector, Conll_prodrop_prediction_selector
from udapi.block.demo.Coreference.CoNLL.conll_predictor import Conll_predictor
from udapi.block.demo.Coreference.CoNLL.conll_coref_adder_new import Conll_coref_adder_new
from udapi.block.demo.Coreference.CoNLL.conll_coref_adder_old  import Conll_coref_adder_old

class Conll_prediction( Block):   
    def __init__( self, rel_model, dem_model, prs_model, prodrop_model, **kwargs):
        super().__init__( **kwargs)
        self.rel_model_name = rel_model
        self.dem_model_name = dem_model
        self.prs_model_name = prs_model
        self.prodrop_model_name = prodrop_model

    def process_document( self, doc):
        self.doc = doc
        self.id_vectors = []
        self.predictor = Conll_predictor()        
       
       # selection of features and prediction for particular pronoun types
        self.selector = Conll_rel_prediction_selector()
        self.select_predict_prontype( self.rel_model_name)

        self.selector = Conll_dem_prediction_selector()
        self.select_predict_prontype( self.dem_model_name)
        
        self.selector = Conll_prs_prediction_selector()
        self.select_predict_prontype( self.prs_model_name) 
           
        self.selector = Conll_prodrop_prediction_selector()
        self.select_predict_prontype( self.prodrop_model_name)                  
        
        # adding the coreference information into CoNLL-U files
        #self.coref_adder = Conll_coref_adder_old()
        self.coref_adder = Conll_coref_adder_new()
        if ( len( self.id_vectors) > 0 ):
            self.coref_adder.add_coreference( self.doc, self.id_vectors)        

    def select_predict_prontype( self, model_name):
        """ prediction of coreference with the given model """
        # selection of features
        self.feature_vectors = []
        super().process_document( self.doc) # -> process node
        
        # prediction
        if ( len( self.feature_vectors) > 0 ):            
            self.id_vectors += self.predictor.predict( self.feature_vectors, model_name)    

    def process_node( self, node):
        """ selection of features """
        self.feature_vectors += self.selector.process_node( node, self.doc)
