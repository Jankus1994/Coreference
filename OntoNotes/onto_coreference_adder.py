# Jan Faryad
# 2. 7. 2017
#
# adding the coreference information into the CoNLL-U file

class Onto_coreference_adder:
    def __init__( self, list_of_clusters):
        cluster_id = -1
        
        # simlpe adding of the coreference information into the nodes
        for cluster in list_of_clusters:
            cluster_id += 1
            for node in cluster.coreferents:
                if ( node != None ):
                    self.add_coreference( node, cluster_id)
    
    def add_coreference( self, node, cluster_id):
        node.misc["Coref"] = str( cluster_id)
