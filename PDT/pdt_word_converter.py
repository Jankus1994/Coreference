# Jan Faryad
#
# 12. 7. 2017

from udapi.block.demo.Coreference.Conv.conv import Conv_word_converter

class Pdt_word_converter( Conv_word_converter):    
    def execute( self, list_of_corefs, list_of_corresponding_words): # -> list of pdt coreferents
        """main conversion method, called from outside"""
        # initialization
        self.list_of_corefs = list_of_corefs
        self.list_of_corresponding_words = list_of_corresponding_words
        #
        
        for coref_record in self.list_of_corefs:
            coref_record.own_node = self.get_corresponding_node( coref_record.own_ID)
            coref_record.coref_node = self.get_corresponding_node( coref_record.coref_ID)         
        
        return self.list_of_corefs
    
    def get_corresponding_node( self, ID_string): # -> udapi node
        """
        finding conll-u ID corresponding to given PDT ID.
        """
        if ( ID_string == None):
            return None
        for i in self.list_of_corresponding_words: 
            if ( i[0][1:] == ID_string[1:] ): # corresponding IDs begin with w, strings with t
                return i[1] # -> node
