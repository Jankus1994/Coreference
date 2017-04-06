# Jan Faryad
#
# Building a matching between words in pdt and conll files

from auxiliaries import get_interstring, transform_ID

class PDT_word_correspondence:
    def __init__( self, pdt_w_input, conllu_input):
        self.pdt_w_input = pdt_w_input
        self.conllu_input = conllu_input
        
        self.para_ID = 0
        self.sent_ID = 1
        
        self.list_of_corresponding_IDs = []
        self.list_of_sentence_IDs = []
        
    def create_correspondence( self):
        """
        main method, called from outside        
        """
        lines_to_omit = 0
        
        for conllu_line in self.conllu_input:
            if ( conllu_line == " \n" ): # a blank line - new sentence                
                self.list_of_sentence_IDs += [ ( self.para_ID, self.sent_ID ) ]
                self.sent_ID += 1
            elif ( conllu_line[0] != '#' ): # not a comment line -> a record line
                
                if ( lines_to_omit > 0 ): # omitting the actual line
                    lines_to_omit -= 1
                    continue
                
                ( pdt_ID, token ) = self.next_pdt_word() # the next word and its ID in the PDT file                 
                
                record_fields = conllu_line.split( '\t')
                ( word_ID, lines_to_omit ) = transform_ID( record_fields[0]) # CoNLL-U IDs in the form like 8-10
                form = record_fields[1]
                
                lines_to_omit += self.token_division( token, form) # spaces and punctuation in the PDT word cause its division in CoNLL-U into more words
                                                             # the pair is built with its first part, other parts ~ lines are omitted                
                conllu_ID = ( self.para_ID, self.sent_ID, word_ID )                      
                self.list_of_corresponding_IDs += [ ( pdt_ID, conllu_ID ) ]
        self.list_of_sentence_IDs += [ ( self.para_ID, self.sent_ID ) ]
        return ( self.list_of_corresponding_IDs, self.list_of_sentence_IDs )
    
    def token_division( self, token, form):
        if ( token == form ):
            return 0
        lines_to_omit = 0
        for char in token:
            if ( char == ' '):
                lines_to_omit += 1
            elif ( char in ",.?!;'-\"" ): # space or punctuation in the token - UDpipe would divide it into more words
                lines_to_omit += 2
        return lines_to_omit
      
    def next_pdt_word( self):
        pdt_line = self.pdt_w_input.readline()
        while ( not "</doc>" in pdt_line ):
            #print(self.para_ID, self.sent_ID )
            #print(pdt_line)            
            if ( "<para" in pdt_line ):
                self.para_ID += 1
                self.sent_ID = 1         
            elif ( "<w id" in pdt_line ):
                pdt_ID = get_interstring( pdt_line, '"', '"')
                token_line = self.pdt_w_input.readline()
                token = get_interstring( token_line, '>', '<')
                return ( pdt_ID, token )
            elif ( pdt_line == "" ):
                return ( "", "" )
            pdt_line = self.pdt_w_input.readline()
        return ( "", "" )