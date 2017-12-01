# Jan Faryad
# 23. 6. 2017
  
class Conll_coref_adder():
    def add_coreference( self, doc, id_vectors):   
        """
        main method for adding detected coreference information
        """     
        self.list_of_coreferents = []
        self.iterator = -1

        # BUILDING CLUSTERS
        for id_vector in id_vectors:      
            #processing input list
            pronoun_node = self.get_node( doc, int( id_vector[0]), int( id_vector[1]))
            antecedent_node = self.get_node( doc, int( id_vector[2]), int( id_vector[3]))
            
            dropped = False
            if ( pronoun_node.upos == "VERB" ):
                dropped = True
        
            # obtaining Coreferents from ids - either creating new coreferents or finding some already existing
            pronoun = self.get_coreferent( pronoun_node, dropped) # these methods could change the list of coreferents            
            antecedent = self.get_coreferent( antecedent_node, False)
            
            # connection between Coreferents
            pronoun.add_coreferent( antecedent)
            antecedent.add_coreferent( pronoun)
                     
        
        # adding cluster id to all Coreferents (and their nodes) in the cluster
        cluster_id = 0        
        for coref in self.list_of_coreferents:                        
            if ( coref.cluster_id == -1 ): # if the cluster still doesn't have an id
                coref.set_cluster_id( cluster_id) # recursion                
                cluster_id += 1 
    
    def get_coreferent( self, node, dropped): # -> Coreferent
        """
        returns Coreferent by id - either existing or it newly created
        """
        coreferents = [ coref for coref in self.list_of_coreferents if ( coref.node == node and coref.dropped == dropped ) ]
        if ( coreferents ):
            return coreferents[0] # at most one such coref
        coreferent = Conll_coreferent( node, dropped)
        self.list_of_coreferents.append( coreferent)
        return coreferent
    
    def get_node( self, doc, sent_id, word_id):
        if ( sent_id <= len( doc.bundles) ):
            bundle = doc.bundles[ sent_id - 1 ]
            if ( bundle.trees ):
                root = bundle.trees[0]
                if ( word_id <= len( root.descendants) ):
                    node = root.descendants[ word_id - 1 ]
                    return node
    
    def next_coreferent( self):
        self.iterator += 1
        if ( len( self.list_of_coreferents) > self.iterator ):
            return self.list_of_coreferents[ self.iterator ]    
    
    def string_to_bool( self, string):
        if ( string == "True"):
            return True
        return False            

class Conll_coreferent:
    def __init__( self, node, dropped): # id ... triplet ( para id, sent id, word id )
        self.node = node
        self.coreferents = []
        self.cluster_id = -1
        self.dropped = dropped
    def add_coreferent( self, coreferent): # void
        if ( coreferent not in self.coreferents ):
            self.coreferents.append( coreferent)
    def set_cluster_id( self, new_cluster_id): # void
        """
        recursive method for setting cluster id to all coreferents in the cluster
        """
        if ( self.cluster_id != new_cluster_id ):
            self.cluster_id = new_cluster_id
            
            if ( self.dropped ):
                self.node.misc['Drop_coref'] = self.cluster_id
            else:
                self.node.misc['Coref'] = self.cluster_id            
            
            for coref in self.coreferents: # recursion
                coref.set_cluster_id( self.cluster_id)
