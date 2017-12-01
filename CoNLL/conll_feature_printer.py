# Jan Faryad
# 17. 11. 2017

from udapi.core.block import Block


from udapi.block.demo.Coreference.CoNLL.conll_rel_training_selector import Conll_rel_training_selector
from udapi.block.demo.Coreference.CoNLL.conll_predictor import Conll_predictor
from udapi.block.demo.Coreference.CoNLL.conll_coref_adder import Conll_coref_adder

class Conll_feature_printer( Block):
    def process_document( self, doc):
        self.doc = doc
        self.selector    = Conll_rel_training_selector()        
        self.feature_vectors = []
        super().process_document( doc)
        for feature_vector in self.feature_vectors:
            #print( '\t'.join( feature_vector))
            for field in feature_vector[:-1]:
                print( field, end = '\t')
            print( feature_vector[-1])
        
    def process_node( self, node):
        self.feature_vectors += self.selector.process_node( node, self.doc)
