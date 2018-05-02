# Jan Faryad
# 19. 6. 2017

"""
The first component of transcription the coreference niformation from PDT files to CoNLL-U
building a matching between PDT word IDs and CoNLL-U nodes
"""

from udapi.block.demo.Coreference.Conv.conv import Conv_word_correspondence
from udapi.block.demo.Coreference.Other.auxiliaries import get_interstring

class Pdt_word_correspondence( Conv_word_correspondence):
    def execute( self, filename, udapi_doc):
        """main method, called from Conv_coref"""
        # initialization
        pdt_w_input = open( filename + ".w", 'r') # surface (word) layer
        list_of_corresponding_words = []     
        #
        
        # creating two lists
        conll_words = []
        pdt_words = []               
        
        # conll
        for bundle in udapi_doc.bundles: # iterating through nodes
            for root in bundle.trees:
                sent_ID = root.sent_id
                for node in root.descendants:                                               
                    word_ID = node.ord
                    form = node.form
                    conll_words.append( ( node, form )) # nodes will be elemements of the bijection (not IDs)
                                                                  # it's simplier as we will add the coreference information to the nodes    
        # pdt
        sent_ID = -1 # numbering from 0
        for  pdt_line in pdt_w_input:
            if ( "<w id" in pdt_line ):
                pdt_ID = get_interstring( pdt_line, '"', '"')
                token_line = pdt_w_input.readline() # the line with the token is always the next line
                token = get_interstring( token_line, '>', '<')
                pdt_words.append( ( pdt_ID, token ))
        
        # building a matching
        # we match pdt ids with Nodes
        FORM = 1
        NODE = 0
        ID  = 0
        
        list_of_corresponding_words = []
        conll_index = 0
        pdt_index = 0
        while ( conll_index < len( conll_words) and pdt_index < len( pdt_words) ):
            conll_word = conll_words[ conll_index ]
            pdt_word = pdt_words[ pdt_index ]
            if ( conll_word[ FORM ] == pdt_word[ FORM ] ):
                list_of_corresponding_words.append( ( pdt_word[ ID ], conll_word[ NODE ] ))
            else: # if the forms differ we search forward the next form in both lists.
                  # we take whichever has the same form with one of the actual words
                i = 1
                limit = 12 # chosen experimentally 
                while ( i < limit and conll_index + i < len( conll_words) and pdt_index + i < len( pdt_words) ):
                    conll_next_word = conll_words[ conll_index + i ]
                    pdt_next_word = pdt_words[ pdt_index + i ]
                    if ( conll_word[ FORM ] == pdt_next_word[ FORM ] ): # we jump over a piece of the pdt list
                        pdt_index += i
                        pdt_word = pdt_next_word
                        break
                    if ( conll_next_word[ FORM ] == pdt_word[ FORM ] ): # we jump over a piece of the conll list
                        conll_index += i
                        conll_word = conll_next_word
                        break
                    i += 1
                list_of_corresponding_words.append( ( pdt_word[ ID ], conll_word[ NODE ] ))
            conll_index += 1
            pdt_index += 1 
        
        pdt_w_input.close()
        return list_of_corresponding_words      
