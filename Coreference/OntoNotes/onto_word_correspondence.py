# Jan Faryad
# 29. 6. 2017
#
# building a matching between words in OntoNotes and CoNLL-U files

class Onto_word_correspondence:
    def __init__( self, onto_input, conll_doc):
        """
        onto input ... onf file
        conll doc ... Document, see udapi
        """
        self.onto_input = onto_input
        self.conll_doc = conll_doc        
        
        self.are_leaves = False # we are readig information about individual words called Leaves
                                # (there are also other blocks of information in the onf file)
        
    def create_correspondence( self):
        """
        main method, called from outside
        it creates two lists of words (for conll file and for onf file) and then builds a bijection based on comparing of forms
        """
        # creating two lists
        conll_words = []
        onto_words = []               
        
        # conll
        for bundle in self.conll_doc.bundles: # iterating through nodes
            for root in bundle.trees:
                sent_ID = root.sent_id
                for node in root.descendants:                                               
                    word_ID = node.ord
                    form = node.form
                    conll_ID = ( sent_ID, word_ID )
                    conll_words.append( ( conll_ID, form, node )) # nodes will be elemements of the bijection (not IDs)
                                                                  # it's simplier as we will add the coreference information to the nodes
        
        # onf (ontonotes)
        sent_ID = -1 # numbering from 0
        for  onto_line in self.onto_input:
            if ( "Leaves:" in onto_line ): # beginning of the "Leaves" section
                self.are_leaves = True
                sent_ID += 1
            elif ( self.are_leaves and onto_line == "\n" ): # end of the "Leaves" section
                self.are_leaves = False          
            elif ( self.are_leaves ): # line in the "Leaves" section
                split_line = onto_line.split( ' ')
                word_ID = None             
                form = None
                try:
                    word_ID = int( split_line[4]) # id begins in fifth column
                    was_number = True
                except:
                    pass # word id remains None                 
                form = split_line[-1][:-1] # last field, except newline
                if ( len( form) == 0 or form[0] == '*' ): # auxiliary token
                    form = None
                
                if ( word_ID != None and form != None ):
                    onto_ID = ( sent_ID, word_ID )
                    onto_words.append( ( onto_ID, form ))
        
        # building a matching
        # we match onto ids with Nodes
        list_of_corresponding_words = []
        conll_index = 0
        onto_index = 0
        while ( conll_index < len( conll_words) and onto_index < len( onto_words) ):
            conll_word = conll_words[ conll_index ]
            onto_word = onto_words[ onto_index ]
            if ( conll_word[1] == onto_word[1] ): # comparing forms
                list_of_corresponding_words.append( ( onto_word[0], conll_word[2] )) # onto_ID, conll node
            else: # if the forms differ we search forward the next form in both lists.
                  # we take whichever has the same form with one of the actual words
                i = 1
                limit = 12 # chosen experimentally 
                while ( i < limit and conll_index + i < len( conll_words) and onto_index + i < len( onto_words) ):
                    conll_sec_word = conll_words[ conll_index + i ]
                    onto_sec_word = onto_words[ onto_index + i ]
                    if ( conll_word[1] == onto_sec_word[1] ): # we jump over a piece of the onto list
                        onto_index += i
                        onto_word = onto_sec_word
                        break
                    if ( conll_sec_word[1] == onto_word[1] ): # we jump over a piece of the conll list
                        conll_index += i
                        conll_word = conll_sec_word
                        break
                    i += 1
                list_of_corresponding_words.append( ( onto_word[0], conll_word[2] )) # onto_ID, conll node
            conll_index += 1
            onto_index += 1 
        
        return list_of_corresponding_words
