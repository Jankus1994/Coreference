# Jan Faryad
# 11. 11. 2017

from udapi.core.block import Block
from udapi.block.demo.Coreference.CoNLL.conll_rel_prediction_selector import Conll_rel_prediction_selector
from udapi.block.demo.Coreference.CoNLL.conll_predictor import Conll_predictor
from udapi.block.demo.Coreference.CoNLL.conll_coref_adder import Conll_coref_adder

class Conll_prediction( Block):   
    def __init__( self, model, **kwargs):
        super().__init__(**kwargs)
        self.model_name = model
    def process_document( self, doc):
        self.doc = doc
        self.selector    = Conll_rel_prediction_selector()
        self.predictor   = Conll_predictor()
        self.coref_adder = Conll_coref_adder()
        
        self.feature_vectors = []
        super().process_document( doc)
        if ( len( self.feature_vectors) > 0 ):
            #print( doc.filename)
            id_vectors = self.predictor.predict( self.feature_vectors, self.model_name)
            self.coref_adder.add_coreference( doc, id_vectors)
        
    def process_node( self, node):
        self.feature_vectors += self.selector.process_node( node, self.doc)
