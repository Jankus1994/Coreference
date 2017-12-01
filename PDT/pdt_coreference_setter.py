# Jan Faryad
# 23. 3. 2017
#
# pdt module for adding coreference into nodes

from udapi.block.demo.Coreference.Conv.conv import Conv_coreference_setter

class Pdt_coreference_setter( Conv_coreference_setter):    
    def execute( self, list_of_corefs):
        """called from outside"""
        # initialization
        self.list_of_corefs = list_of_corefs
        self.list_of_cluster_records = []
        self.cluster_id = -1 # id of coreference clusters    
        #
        
        for record in self.list_of_corefs:      
            cluster_ID = self.find_coref_cluster( record.coref_node, record.coref_dropped)
            
            if ( cluster_ID == None ):
                # only for heads of the chains - their referents must be process seperately, as their don't have their own records
                cluster_ID = self.new_cluster()
                coref_cluster_record = Cluster_record( record.coref_node, cluster_ID, record.coref_dropped)
                self.set_cluster( record.coref_node, cluster_ID, record.coref_dropped)
                self.list_of_cluster_records.append( coref_cluster_record)
            
            own_cluster_record = Cluster_record( record.own_node, cluster_ID, record.own_dropped)
            self.set_cluster( record.own_node, cluster_ID, record.own_dropped)
            self.list_of_cluster_records.append( own_cluster_record)
        
        #for cluster_record in self.list_of_cluster_records:
        #    if ( cluster_record.dropped ):
        #        cluster_record.node.misc["Drop_coref"] = cluster_record.cluster_ID
        #    else:
        #        cluster_record.node.misc["Coref"] = cluster_record.cluster_ID
            
    def find_coref_cluster( self, node, dropped): # -> int (cluster number)
        """
        if this cluster was already used, returns its number. otherwise None - then will the caller set up a new cluster
        """
        for record in self.list_of_cluster_records:
            if ( record.node == node and record.dropped == dropped):
                return record.cluster_ID
        return None
    
    def new_cluster( self):
        self.cluster_id += 1
        return self.cluster_id
    
    def set_cluster( self, node, cluster_ID, dropped):
        if ( node == None ):
            return
        
        if ( dropped ):
            node.misc["Drop_coref"] = cluster_ID
        else:
            node.misc["Coref"] = cluster_ID
    
class Cluster_record:
    def __init__( self, node, cluster_ID, dropped):
        self.node = node
        self.cluster_ID = cluster_ID
        self.dropped = dropped
