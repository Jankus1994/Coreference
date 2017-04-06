# Jan Faryad
#
# conversion od PDT word IDs of coreferents to conll-u word IDs

class PDT_ID_conversion:
    def __init__( self, list_of_corefs_in, list_of_corresponding_IDs):
        self.list_of_corefs_in = list_of_corefs_in
        self.list_of_corefs_out = []
        self.list_of_corresponding_IDs = list_of_corresponding_IDs
    
    def convert_IDs( self): # -> list of coreference records
        """
        main conversion method, called from outside
        """
        for coref_record in self.list_of_corefs_in:
            # changing attributes own_ID and coref_ID from strings to triplets
            coref_record.own_ID = self.get_corresponding_ID( coref_record.own_ID)
            coref_record.coref_ID = self.get_corresponding_ID( coref_record.coref_ID)         
            
            self.insert_coref_record( coref_record)
        return self.list_of_corefs_out
    
    def get_corresponding_ID( self, ID_string): # -> triplet (para ID, sent ID, word ID)
        """
        finding conll-u ID corresponding to given PDT ID.
        """
        if ( ID_string == None):
            return None
        for i in self.list_of_corresponding_IDs: 
            if ( i[0][1:] == ID_string[1:] ): # corresponding IDs begin with w, strings with t
                return i[1]
            
    def insert_coref_record( self, coref_record):
        """
        inserting transformord coreference record to the output list.
        records were ordered according to the pre-order number in pdt trees, now will be sorted according to the the order in the text
        """
        if ( coref_record.own_ID == None or coref_record.coref_ID == None ):
            return # coreference includes t-node that hasn't w-node parent (they are represented by sentence ID)
        if ( len( self.list_of_corefs_out) == 0 ): # empty list
            self.list_of_corefs_out = [ coref_record ]
        else:            
            for i in range( len( self.list_of_corefs_out)):
                if ( self.list_of_corefs_out[i].own_ID > coref_record.own_ID): # insert according to the order of words in the text
                    self.list_of_corefs_out = self.list_of_corefs_out[:i] + [ coref_record ] + self.list_of_corefs_out[i:]
                    break
            else:
                self.list_of_corefs_out += [ coref_record ]       
