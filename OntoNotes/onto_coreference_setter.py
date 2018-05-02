# Jan Faryad
# 2. 7. 2017
#
# the fourth part of transfering the coreference information: adding it into the CoNLL-U file

from udapi.block.demo.Coreference.Conv.conv import Conv_coreference_setter

class Onto_coreference_setter( Conv_coreference_setter):
    def execute( self, list_of_onto_clusters):
        self.cluster_id = -1
        
        # simlpe adding of the coreference information into the nodes
        for cluster in list_of_onto_clusters:
            if ( len( cluster.node_coreferents) > 1 ):
                self.cluster_id += 1
                for node in cluster.node_coreferents:
                    if ( node != None ):
                        self.add_coreference( node)
    
    def add_coreference( self, node):
        node.misc["Coref"] = str( self.cluster_id)
