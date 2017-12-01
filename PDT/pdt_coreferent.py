# Jan Faryad]
# 12. 7. 2017

class Pdt_coreferent():
    def __init__( self, own_dropped, own_ID, coref_dropped, coref_ID):
        self.own_dropped = own_dropped # bool - if the refering word is dropped
        self.coref_dropped = coref_dropped # bool - if the referent is dropped
        
        self.own_ID = own_ID # id string of the refering word
        self.coref_ID = coref_ID # id string of the referent     
        
        self.own_node = None
        self.coref_node = None
        
        self.cluster_ID = -1
