# Jan Faryad
# 2. 7. 2017
#
# adding the coreference information into the CoNLL-U file

class Onto_coreference_adder:
    def __init__( self, list_of_clusters, init_cluster_id):
        self.cluster_id = init_cluster_id
        
        # simlpe adding of the coreference information into the nodes
        for cluster in list_of_clusters:
            self.cluster_id += 1
            for node in cluster.coreferents:
                if ( node != None ):
                    self.add_coreference( node)
    
    def add_coreference( self, node):
        node.misc["Coref"] = str( self.cluster_id)
