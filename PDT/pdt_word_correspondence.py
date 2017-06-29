# Jan Faryad
# 19. 6. 2017

from udapi.block.demo.Coreference.Other.auxiliaries import get_interstring

punctuation = ",.?!;'-\""

class PDT_word_correspondence:
    def __init__( self, pdt_w_input, conll_doc):
        self.pdt_w_input = pdt_w_input
        self.conll_doc = conll_doc
        
        self.para_ID = 0
        self.sent_ID = 0
        
        self.list_of_corresponding_IDs = []
        self.list_of_sentence_IDs = []
        
    def create_correspondence( self):
        """
        main method, called from outside        
        """
        nodes_to_omit = 0
        for bundle in self.conll_doc.bundles:
            for root in bundle.trees:         
                for node in root.descendants:
                    if ( nodes_to_omit > 0 ):
                        nodes_to_omit -= 1
                        continue
                    
                    if ( node.multiword_token != None ): # originally one token, divided by UDPipe into multiple nodes. for the matching we use only 
                                                         # the first node, the rest must be omitted
                        nodes_to_omit += len( node.multiword_token.words) - 1                                  
                    
                    word_ID = node.ord
                    form = node.form
                    
                    ( pdt_ID, token ) = self.next_pdt_word() # the next word and its ID in the PDT file
                    
                    
                    nodes_to_omit += self.token_division( token, form) # spaces and punctuation in the PDT word cause its division in CoNLL-U into more words
                    # for the matching we use only the first node, the rest must be omitted
                    conll_ID = ( self.para_ID, self.sent_ID, word_ID )
                    self.list_of_corresponding_IDs += [ ( pdt_ID, conll_ID ) ]                                    
                self.list_of_sentence_IDs += [ ( self.para_ID, self.sent_ID ) ] 
                self.sent_ID += 1
        return ( self.list_of_corresponding_IDs, self.list_of_sentence_IDs )
    
    def token_division( self, token, form): # -> int
        """
        space or punctuation in the token - UDpipe divides it into more nodes
        """
        if ( token == form ):
            return 0
        lines_to_omit = 0
        for char in token:
            if ( char == ' '): # space divides the token into two parts
                lines_to_omit += 1
            elif ( char in punctuation ): # punctuation into three (the punctuation sign itself forms also a node)
                lines_to_omit += 2
        return lines_to_omit    
      
    def next_pdt_word( self): # -> ( pdt_ID (string), pdt token form (string) )
        pdt_line = self.pdt_w_input.readline()
        while ( not "</doc>" in pdt_line ):       
            if ( "<para" in pdt_line ): # new paragraph
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
