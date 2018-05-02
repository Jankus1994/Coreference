# Jan Faryad
# 23. 3. 2017
#
# The fourth pdt module - for adding the coreference information into nodes

from udapi.block.demo.Coreference.Conv.conv import Conv_coreference_setter
import logging

class Pdt_coreference_setter( Conv_coreference_setter):    
    def execute( self, list_of_corefs):
        """
        called from outside
        list of corefs - list of Pdt_coreferent
        """
        # initialization
        self.cluster_coreferents = []
        #
        for pdt_coreferent in list_of_corefs:
            target_cluster_coreferent = self.get_cluster_coreferent( pdt_coreferent.coref_node, pdt_coreferent.coref_dropped)  
            own_cluster_coreferent = self.get_cluster_coreferent( pdt_coreferent.own_node, pdt_coreferent.own_dropped)
            
            target_cluster_coreferent.add_coreferent( own_cluster_coreferent) # establishing connection between the coreferents
            own_cluster_coreferent.add_coreferent( target_cluster_coreferent) # in both directions - in Pdt_coreferents there was only one direction

        cluster_id = -1 # id of coreference clusters         
        for cluster_coreferent in self.cluster_coreferents:
            if ( cluster_coreferent.cluster_ID == -1 ):
                cluster_id += 1
                cluster_coreferent.set_cluster_id( cluster_id)
            
    def get_cluster_coreferent( self, node, dropped): # -> cluster record
        """ finding cluster coreferent if this cluster was already used, returns it. otherwise will create a new one """
        for cluster_coreferent in self.cluster_coreferents:
            if ( cluster_coreferent.node == node and cluster_coreferent.dropped == dropped):
                return cluster_coreferent
        new_cluster_coreferent = Cluster_coreferent( node, dropped)
        self.cluster_coreferents.append( new_cluster_coreferent)
        return new_cluster_coreferent


class Cluster_coreferent:
    """class representing coreferent as a part of a coreference cluster"""
    def __init__( self, node, dropped):
        self.node = node
        self.corefering_cluster_coreferents = [] # in comparision with Pdt_coreferent there can be more of them
        self.cluster_ID = -1
        self.dropped = dropped
    def add_coreferent( self, coreferent):
        self.corefering_cluster_coreferents.append( coreferent)
    def set_cluster_id( self, cluster_id):
        if ( self.cluster_ID != cluster_id  ):
            self.cluster_ID = cluster_id
            for coref_cluster_record in self.corefering_cluster_coreferents:
                coref_cluster_record.set_cluster_id( cluster_id)
            if ( len( self.corefering_cluster_coreferents) > 0 ): # it could happend, that coreferent was a dropped child of technical sentence root
                if ( self.dropped ):
                    self.node.misc["Drop_coref"] = self.cluster_ID
                else:
                    self.node.misc["Coref"] = self.cluster_ID
              
