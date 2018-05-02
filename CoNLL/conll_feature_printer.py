# Jan Faryad
# 10. 3. 2018

from udapi.core.block import Block
from udapi.block.demo.Coreference.CoNLL.conll_specific_selectors import Conll_rel_training_selector, Conll_dem_training_selector, Conll_prs_training_selector
import logging

class Conll_feature_printer( Block):
    """
    prints features for training (ie. with a target value) to standard output
    general class, to be overloaded with classes for individual pronoun types
    """
    def __init__( self, **kwargs):
        super().__init__( **kwargs)
        self.selector = None # to be overloaded
    def process_document( self, doc):
        # initializatiion
        self.doc = doc
        logging.info( str( doc.filename))
        self.feature_vectors = []
        
        # running method process_node for each node
        super().process_document( doc)        
        
        # printing
        for feature_vector in self.feature_vectors:
            for field in feature_vector[:-1]:
                print( field, end = '\t')
            print( feature_vector[-1])
        
    def process_node( self, node):
        """ appending feature vectors for one node to the general list """
        self.feature_vectors += self.selector.process_node( node, self.doc)
        
