# Jan Faryad
# 23. 3. 2017
#
# pdt module to conversion of the coreferennce information from chains to clusters

class PDT_clusterization:    
    def __init__( self, list_of_corefs, init_cluster_id):
        self.list_of_corefs = list_of_corefs
        self.list_of_cluster_tuples = []
        self.cluster_id = init_cluster_id # id of coreference clusters        
    
    def convert_chains_to_clusters( self):
        """
        called from outside
        """
        for record in self.list_of_corefs:
            cluster_ID = self.find_coref_cluster( record.coref_ID)
            if ( cluster_ID == None ):
                # only for heads of the chains - their referents must be process seperately, as their don't have their own records
                cluster_ID = self.new_cluster()
                coref_cluster_record = (
                    record.coref_ID[0], record.coref_ID[1], record.coref_ID[2], cluster_ID, record.coref_dropped)
                    # paragraph ID,     sentence ID,        word ID
                self.list_of_cluster_tuples.append( coref_cluster_record)
            own_cluster_record = (
                record.own_ID[0], record.own_ID[1], record.own_ID[2], cluster_ID, record.own_dropped)#, record.perspron)
                # paragraph ID,     sentence ID,        word ID
            self.list_of_cluster_tuples.append( own_cluster_record)
            
        self.list_of_cluster_tuples = sorted( self.list_of_cluster_tuples)
        
        list_of_cluster_records = [] # building object-records from tuples
        for tuple in self.list_of_cluster_tuples:
            cluster_record = Cluster_record( tuple)
            list_of_cluster_records.append( cluster_record)
        return list_of_cluster_records
            
    def find_coref_cluster( self, ids): # -> int (cluster number)
        """
        if this cluster was already used, returns its number. otherwise None - then will the caller set up a new cluster
        """
        for tuple in self.list_of_cluster_tuples:
            if ( ( tuple[0], tuple[1], tuple[2] ) == ids ):
                return tuple[3]
        return None
    
    def new_cluster( self):
        self.cluster_id += 1
        return self.cluster_id
    
    def get_cluster_id( self):
        return self.cluster_id
    
class Cluster_record:
    def __init__( self, tuple):
        self.para_ID = tuple[0]
        self.sent_ID = tuple[1]
        self.word_ID = tuple[2]
        self.cluster_ID = tuple[3]
        self.dropped = tuple[4]
        #self.perspron
    
