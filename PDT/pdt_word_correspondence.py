# Jan Faryad
# 19. 6. 2017

from udapi.block.demo.Coreference.Conv.conv import Conv_word_correspondence
from udapi.block.demo.Coreference.Other.auxiliaries import get_interstring

class Pdt_word_correspondence( Conv_word_correspondence):
    def execute( self, filename, udapi_doc):
        """main method, called from outside"""
        # initialization
        pdt_w_input = open( filename + ".w", 'r') # surface (word) layer
        udapi_doc = udapi_doc        
        list_of_corresponding_words = []     
        #self.punctuation = ",.?!;'-\""
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
                    conll_ID = ( sent_ID, word_ID )
                    conll_words.append( ( conll_ID, form, node )) # nodes will be elemements of the bijection (not IDs)
                                                                  # it's simplier as we will add the coreference information to the nodes
    
        # pdt
        sent_ID = -1 # numbering from 0
        for  pdt_line in pdt_w_input:
            if ( "<w id" in pdt_line ):
                pdt_ID = get_interstring( pdt_line, '"', '"')
                token_line = pdt_w_input.readline()
                token = get_interstring( token_line, '>', '<')
                pdt_words.append( ( pdt_ID, token ))

        
        # building a matching
        # we match pdt ids with Nodes
        list_of_corresponding_words = []
        conll_index = 0
        pdt_index = 0
        while ( conll_index < len( conll_words) and pdt_index < len( pdt_words) ):
            conll_word = conll_words[ conll_index ]
            pdt_word = pdt_words[ pdt_index ]
            if ( conll_word[1] == pdt_word[1] ): # comparing forms
                list_of_corresponding_words.append( ( pdt_word[0], conll_word[2] )) # pdt_ID, conll node
            else: # if the forms differ we search forward the next form in both lists.
                  # we take whichever has the same form with one of the actual words
                i = 1
                limit = 12 # chosen experimentally 
                while ( i < limit and conll_index + i < len( conll_words) and pdt_index + i < len( pdt_words) ):
                    conll_sec_word = conll_words[ conll_index + i ]
                    pdt_sec_word = pdt_words[ pdt_index + i ]
                    if ( conll_word[1] == pdt_sec_word[1] ): # we jump over a piece of the pdt list
                        pdt_index += i
                        pdt_word = pdt_sec_word
                        break
                    if ( conll_sec_word[1] == pdt_word[1] ): # we jump over a piece of the conll list
                        conll_index += i
                        conll_word = conll_sec_word
                        break
                    i += 1
                list_of_corresponding_words.append( ( pdt_word[0], conll_word[2] )) # pdt_ID, conll node
            conll_index += 1
            pdt_index += 1 
        
        pdt_w_input.close()
        return list_of_corresponding_words      
