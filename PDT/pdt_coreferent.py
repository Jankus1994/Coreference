# Jan Faryad
# 12. 7. 2017
#
# Class representing a corefering word in the text. At the beginning, the coreference is described with PDT IDs, later with CoNLL-U nodes and at the end with a cluster number

class Pdt_coreferent():
    def __init__( self, own_dropped, own_ID, coref_dropped, coref_ID):
        self.own_dropped = own_dropped # bool - if the refering word is dropped
        self.coref_dropped = coref_dropped # bool - if the referent is dropped
        
        self.own_ID = own_ID # id string of the refering word
        self.coref_ID = coref_ID # id string of the referent     
        
        self.own_node = None
        self.coref_node = None
        
        self.coreferents_in_cluster = [] # Pdt_coreferents corefering with this one
        self.cluster_ID = -1

    
    def set_own_node( self, node):
        self.own_node = node
    def set_coref_node( self, node):
        self.coref_node = node
