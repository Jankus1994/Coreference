# Jan Faryad
# 23. 6. 2017

from math import fabs
import logging
  
class Conll_coref_adder_new():
    def add_coreference( self, doc, id_vectors):   
        """ main method for adding detected coreference information """     
        self.list_of_coreferents = []
        list_of_pronoun_coreferents = []
        self.iterator = -1

        # BUILDING CLUSTERS
        for id_vector in id_vectors:      
            # processing input list
            pronoun_node = self.get_node( doc, int( id_vector[0]), int( id_vector[1]))
            candidate_node = self.get_node( doc, int( id_vector[2]), int( id_vector[3]))
            
            dropped = False
            if ( pronoun_node.upos == "VERB" ):
                dropped = True
        
            # obtaining Conll_coreferents from ids - either creating new coreferents or finding some already existing
            pronoun_coreferent = self.get_coreferent( pronoun_node, dropped) # these methods could change the list of coreferents            
            candidate_coreferent = self.get_coreferent( candidate_node, False)
            
            pronoun_coreferent.add_coreferent( candidate_coreferent) # a pronoun coreferent has a list of possible candidate coreferents
            if ( pronoun_coreferent not in list_of_pronoun_coreferents):
                list_of_pronoun_coreferents.append( pronoun_coreferent)

        for pronoun_coreferent in  list_of_pronoun_coreferents:
            # each pronoun coreferent selects one of its possible candidates - the closest one, the list of coreferents becomes empty
            pronoun_coreferent.get_closest_coreferent()
            
        for pronoun_coreferent in  list_of_pronoun_coreferents:
            closest_coreferent = pronoun_coreferent.closest_coreferent
            # creates a 1:1 connection between pronoun and its closest coreferent
            # still multiword clusters can appear - multiple pronouns could refer to the same candidate or a pronoun itself could be the closest candidate for another pronoun
            pronoun_coreferent.add_coreferent( closest_coreferent)
            closest_coreferent.add_coreferent( pronoun_coreferent)
        
        # assigning a number to the clusters
        cluster_id = 0        
        for pronoun_coreferent in  list_of_pronoun_coreferents:
            if ( pronoun_coreferent.cluster_id == -1 ): # if the cluster still doesn't have an id
                pronoun_coreferent.set_cluster_id( cluster_id) # recursion - asigning cluster id to all corefering nodes                
                cluster_id += 1 
    
    def get_coreferent( self, node, dropped): # -> Conll_coreferent
        """ returns Conll_coreferent by node and dropped-information - either existing or newly created """
        coreferents = [ coref for coref in self.list_of_coreferents if ( coref.node == node and coref.dropped == dropped ) ]
        if ( coreferents ):
            return coreferents[0] # at most one such coreferent
        coreferent = Conll_coreferent( node, dropped)
        self.list_of_coreferents.append( coreferent)
        return coreferent
    
    def get_node( self, doc, sent_id, word_id): # -> udapi node
        """ gets udapi node by ID """
        if ( sent_id <= len( doc.bundles) ):
            bundle = doc.bundles[ sent_id - 1 ]
            if ( bundle.trees ):
                root = bundle.trees[0] # there should be only one tree in the bundle
                if ( word_id <= len( root.descendants) ):
                    node = root.descendants[ word_id - 1 ]
                    return node
        
class Conll_coreferent:
    """ object representing a node as a corefering entity """
    def __init__( self, node, dropped): # so one node can correspond to two coreferents - one non-dropped and one representing a dropped pronoun
        self.node = node
        self.dropped = dropped
        
        self.coreferents = []
        self.closest_coreferent = None
        self.cluster_id = -1        
        # IDs
        self.sent_id = int( node.root.sent_id)
        self.word_id = int( node.ord)
    def add_coreferent( self, coreferent): # void
        if ( coreferent not in self.coreferents ):
            self.coreferents.append( coreferent)
    def set_cluster_id( self, new_cluster_id): # void
        """ recursive method for setting cluster id to all coreferents in the cluster """
        if ( self.cluster_id != new_cluster_id ):
            self.cluster_id = new_cluster_id
            
            if ( self.dropped ):
                self.node.misc[ "Drop_coref" ] = self.cluster_id
            else:
                self.node.misc[ "Coref" ] = self.cluster_id            
            
            for coref in self.coreferents: # recursion
                coref.set_cluster_id( self.cluster_id)
                
    def get_closest_coreferent( self):
        coref_ids = [] # ids of possible coreferents
        for coref in self.coreferents:
            coref_ids.append( ( int( coref.sent_id), int( coref.word_id) ))
        coref_ids.append( ( self.sent_id, self.word_id )) # we add ID of this node
        coref_ids.sort()
        
        # from a sorted list we pick the node (resp., its ID) before and after this one
        prev_coref_id = None
        next_coref_id = None
        for i in range( len( coref_ids)):
            if ( coref_ids[i] == ( self.sent_id, self.word_id) ):
                if ( i != 0 ):
                    prev_coref_id = coref_ids[ i - 1 ]
                if ( i != len( coref_ids) - 1 ):
                    next_coref_id =  coref_ids[ i + 1 ]
                break
        # if all candidates are after / before this pronoun, then the closest one is clear
        if ( prev_coref_id == None ):
            closest_coref_id = next_coref_id
        elif ( next_coref_id == None ):
            closest_coref_id = prev_coref_id
        else:
            # else we have to chose whuich one is closer - first according to the sentence ID
            if ( self.sent_id - prev_coref_id[0] < next_coref_id[0] - self.sent_id ):
                closest_coref_id = prev_coref_id
            elif ( self.sent_id - prev_coref_id[0] > next_coref_id[0] - self.sent_id ):
                closest_coref_id = next_coref_id        
            else: # both are in the same sentence as the pronoun -> we are choosing according to word ID
                if ( self.word_id - prev_coref_id[1] <= next_coref_id[1] - self.word_id ): # if the distance of both is equal, we prefere the previous one
                    closest_coref_id = prev_coref_id
                else: # ( self.word_id - prev_coref_id[1] > next_coref_id[1] - self.word_id ):
                    closest_coref_id = next_coref_id     
                    
        self.closest_coreferent = [ coref for coref in self.coreferents if int( coref.sent_id) == closest_coref_id[0] and int( coref.word_id) == closest_coref_id[1] ][ 0 ]
        self.coreferents = []

