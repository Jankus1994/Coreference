# Jan Faryad
# 11. 12. 2016
#
# Program for adding the given coreference information into a CoNLL-U file
# moreover, it adds a sentence ID in front of each sentence
# !!! version with clusters

from udapi.block.demo.Coreference.Other.auxiliaries import join_with_separator, transform_ID

class PDT_add_coreference():    
    def __init__( self, list_of_corefs, list_of_sentence_IDs, conll_doc):
        self.list_of_corefs = list_of_corefs # list of coreference records, see PDT_get_coref
        self.list_of_sentence_IDs = list_of_sentence_IDs # list of pairs ( paragraph ID, sentence ID in the paragraph )
        self.conll_doc = conll_doc
        
        self.coref_index = 0 # position in the list of coreference records
        self.actual_coref_record = list_of_corefs[ self.coref_index ] # the first record
        self.sentence_index = 0 # position in the list of sentence IDs
        ( self.para_ID, self.sent_ID ) = self.list_of_sentence_IDs[ self.sentence_index ] # ID of the first sentence
        self.word_ID = 0 # ID of the word in a sentence
    
    def process_file( self): # void
        """
        main method for adding - run from outside
        iterating all the nodes and controlling, which of them have a coreference record in the list
        """        
        for bundle in self.conll_doc.bundles:
            for root in bundle.trees:
                self.next_sentence()
                for node in root.descendants:                    
                    self.word_ID = node.ord
                    if ( self.compare_coref_position() ): # if the actual position in the input equals the position with the next coreference
                        while ( self.compare_coref_position() ): # there can be more coreferences in one node - if its coreferenting subnodes are missing at the surface layer
                            self.add_coreference( node)
                            self.next_coref()
    
    def next_coref( self): # void
        """
        moving to the next coreference record in the list
        """
        if ( self.coref_index + 1 <  len( self.list_of_corefs) ):
            self.coref_index += 1
            self.actual_coref_record = self.list_of_corefs[ self.coref_index ]
        else:
            self.actual_coref_record = None
            
    def add_coreference( self, node): # void
        """
        adding the information from the actual record to the given node
        """
        coref_attribute = self.get_coref_attribute() # coref / drop coref
        coref_value = str( self.actual_coref_record.cluster_ID)
        node.misc[coref_attribute] = coref_value
    
    def get_coref_attribute( self): # -> string
        if ( not self.actual_coref_record.dropped ):
            return "Coref" # coreferent is represented in the surface layer
        else: # ( self.actual_coref_record.dropped ):
            return "Drop_coref" # coreferent is dropped
    
    def next_sentence( self): # void
        """
        getting the next sentence ID
        """
        ( self.para_ID, self.sent_ID ) = self.list_of_sentence_IDs[ self.sentence_index ]
        self.sentence_index += 1
        self.word_ID = 0
    
    def compare_coref_position( self): # -> bool
        """
        controlling if the actual position corresponds to the position of the next word with coreference information
        """
        if ( self.actual_coref_record == None ): # the last coreference record was already processed
            return False      
        return ( self.actual_coref_record.para_ID == self.para_ID # returning the bool value
                and self.actual_coref_record.sent_ID == self.sent_ID
                and self.actual_coref_record.word_ID == self.word_ID
                )
