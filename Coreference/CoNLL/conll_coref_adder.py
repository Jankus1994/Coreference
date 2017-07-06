# Jan Faryad
# 23. 6. 2017

from udapi.core.block import Block
import sys

class Conll_coref_adder( Block):    
    def process_document( self, doc):   
        """
        main method for adding detected coreference information
        """     
        self.list_of_coreferents = []
        self.iterator = -1
        
        # READING INPUT AND BUILDING CLUSTERS
        for line in sys.stdin:            
            #processing input
            fields = line[:-1].split( '\t')
            pronoun_id = ( int( fields[0]), int( fields[1]) )
            antecedent_id = ( int( fields[2]), int( fields[3]) )
            are_coreferents = self.string_to_bool( fields[4])
        
            # creating coreferents and connections between them
            if ( are_coreferents ): # if they are coreferents
                # obtaining Coreferents from ids - either creating new coreferents or finding some already existing
                pronoun = self.get_coreferent( pronoun_id) # these methods could change the list of coreferents
                antecedent = self.get_coreferent( antecedent_id)
                # connection between Coreferents
                pronoun.add_coreferent( antecedent)
                antecedent.add_coreferent( pronoun)
                
        # adding cluster id to all Coreferents in the cluster
        cluster_id = 0
        for coref in self.list_of_coreferents:
            if ( coref.cluster_id == -1 ): # if the cluster still doesn't have an id
                coref.rewrite_cluster_id( cluster_id) # recursion                
                cluster_id += 1
                
        # ADDING CLUSTER IDS TO NODES
        actual_coreferent = self.next_coreferent()      
        for bundle in doc.bundles:
            sent_id = int( bundle.bundle_id)
            for root in bundle.trees:                
                for node in root.descendants:
                    if ( actual_coreferent == None ): # no more coreferents in the document
                        return
                    #print( actual_coreferent.id, ( sent_id, node.ord ) )
                    if ( actual_coreferent.id == ( sent_id, node.ord ) ):
                        #print("tuu")
                        node.misc['Coref'] = actual_coreferent.cluster_id
                        actual_coreferent = self.next_coreferent()
        
    
    def get_coreferent( self, coreferent_id): # -> Coreferent
        """
        returns Coreferent by id - either existing or it newly created
        """
        for i in range( len( self.list_of_coreferents)):
            if ( coreferent_id < self.list_of_coreferents[i].id ): # new coreferent in the middle
                coreferent = Conll_coreferent( coreferent_id)
                self.list_of_coreferents = self.list_of_coreferents[:i] + [ coreferent ] + self.list_of_coreferents[i:]
                return coreferent
            elif ( coreferent_id == self.list_of_coreferents[i].id ): # existing coreferent
                return self.list_of_coreferents[i]
        coreferent = Conll_coreferent( coreferent_id) # new coreferent at the end
        self.list_of_coreferents.append( coreferent)
        return coreferent
    
    def next_coreferent( self):
        self.iterator += 1
        if ( len( self.list_of_coreferents) > self.iterator ):
            return self.list_of_coreferents[ self.iterator ]    
    
    def string_to_bool( self, string):
        if ( string == "True"):
            return True
        return False            

class Conll_coreferent:
    def __init__( self, id): # id ... triplet ( para id, sent id, word id )
        self.id = id
        self.coreferents = []
        self.cluster_id = -1
    def add_coreferent( self, coreferent): # void
        if ( coreferent not in self.coreferents ):
            self.coreferents.append( coreferent)
    def rewrite_cluster_id( self, new_cluster_id): # void
        """
        recursive method for setting cluster id to all coreferents in the cluster
        """
        if ( self.cluster_id != new_cluster_id ):
            self.cluster_id = new_cluster_id
            for coref in self.coreferents:
                coref.rewrite_cluster_id( self.cluster_id)
