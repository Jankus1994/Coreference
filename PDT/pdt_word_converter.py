# Jan Faryad
# 12. 7. 2017
#
# Third part of PDT coref conversion - converting the coreference information in the form of PDT IDs to CoNLL-U nodes using a given matching

from udapi.block.demo.Coreference.Conv.conv import Conv_word_converter

class Pdt_word_converter( Conv_word_converter):    
    def execute( self, list_of_pdt_coreferents, list_of_corresponding_words): # -> list of pdt coreferents
        """main conversion method, called from outside"""
        # initialization
        self.list_of_pdt_coreferents = list_of_pdt_coreferents # list of Pdt_coreferent
        self.list_of_corresponding_words = list_of_corresponding_words # list of pairs ( PDT ID : string, CoNLL-U Node )

        # proper conversion of the ID of the pronoun and of its coreferent to nodes
        for pdt_coreferent in self.list_of_pdt_coreferents:
            own_node = self.get_corresponding_node( pdt_coreferent.own_ID)            
            pdt_coreferent.set_own_node( own_node)
            coref_node = self.get_corresponding_node( pdt_coreferent.coref_ID)  
            pdt_coreferent.set_coref_node( coref_node)
        
        return [ pdt_coreferent for pdt_coreferent in self.list_of_pdt_coreferents if ( pdt_coreferent.own_node != None and pdt_coreferent.coref_node != None ) ] # some coreferents are artificial children of technical sentence root
    
    def get_corresponding_node( self, ID_string): # -> udapi node
        """
        finding conll-u ID corresponding to given PDT ID.
        """
        if ( ID_string == None):
            return None
        for i in self.list_of_corresponding_words: 
            if ( i[0][1:] == ID_string[1:] ): # IDs matched with nodes begin with w, ID strings of coreference with t, because they are obtained from PDT w-files, resp. t-files
                return i[1] # -> node
