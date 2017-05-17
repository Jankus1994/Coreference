# Jan Faryad
# 11. 12. 2016
#
# Program for adding the given coreference information into a CoNLL-U file
# moreover, it adds a sentence ID in front of each sentence
# !!! version with clusters

from auxiliaries import join_with_separator, transform_ID

class PDT_add_coreference():    
    def __init__( self, list_of_corefs, list_of_sentence_IDs, conllu_input, conllu_output_coref, conllu_output_plain):
        self.list_of_corefs = list_of_corefs # list of coreference records, see PDT_get_coref
        self.list_of_sentence_IDs = list_of_sentence_IDs # list of pairs ( paragraph ID, sentence ID in the paragraph )
        self.conllu_input = conllu_input # input file
        self.conllu_output_coref = conllu_output_coref # output file with marked coreference
        self.conllu_output_plain = conllu_output_plain # output file without coreference - only sentence ids added
        
        self.coref_index = 0 # position in the list of coreference records
        self.actual_coref_record = list_of_corefs[ self.coref_index ] # the first record
        self.sentence_index = 0 # position in the list of sentence IDs
        ( self.para_ID, self.sent_ID ) = self.list_of_sentence_IDs[ self.sentence_index ] # ID of the first sentence
        self.word_ID = 0 # ID of the word in a sentence
    
    def process_file( self): # void
        """
        main method for adding - run from outside
        """
        self.next_sentence() # first sentence
        self.write_sentnce_id() # print its ID to the output
        for line in self.conllu_input:
            if ( line == " \n" or line == "\n" ): # a new sentence
                self.conllu_output_coref.write( " \n") # preserving a space on blank lines
                self.conllu_output_plain.write( " \n")
                self.next_sentence()
                self.write_sentnce_id()
            elif ( line[0] == '#' ): # comment line beginning with #
                self.conllu_output_coref.write( line)
                self.conllu_output_plain.write( line)
            else: # record line
                self.conllu_output_plain.write( line) # we don't change lines for plain output
                word_ID_string = line.split( '\t')[0]
                ( self.word_ID, lines_to_omit ) = transform_ID( word_ID_string) # some of IDs are an interval, not a number
                if ( self.compare_coref_position() ): # if the actual position in the input equals the position with the next coreference
                    while ( self.compare_coref_position() ): # there can be more coreferences in one node - if its coreferenting subnodes are missing at the surface layer
                        line = self.add_coreference( line)
                        self.next_coref()
                    self.conllu_output_coref.write( line)
                    # we take only the first record and ignore the others - for our purpose, there are no such cases                                     
                    # new_line = self.add_coreference( line)
                    # self.conllu_output.write( new_line)             
                    # while ( self.compare_coref_position() ): # there can be more coreferences in one node - if its coreferenting subnodes are missing at the surface layer
                    #     self.next_coref()
                else:
                    self.conllu_output_coref.write( line)
    
    def next_coref( self): # void
        """
        moving to the next coreference record in the list
        """
        if ( self.coref_index + 1 <  len( self.list_of_corefs) ):
            self.coref_index += 1
            self.actual_coref_record = self.list_of_corefs[ self.coref_index ]
        else:
            self.actual_coref_record = None
            
    def add_coreference( self, line): # -> string
        """
        adding the information from the actual record to the actual line
        """
        coref_info = self.get_coref_info() # string to be added
        line_list = line.split('\t') # list of fields
        misc = line_list[-1] # adding to the last column
        if ( misc == "_\n" or misc == "_" ): # no other information in the column
            new_misc = coref_info + "\n"
        else: # adding to another information
            new_misc = misc[:-1] + "|" + coref_info + "\n" # [:-1] ... except newline
        new_line = join_with_separator( line_list[:-1] + [ new_misc ], '\t') # rebuildng the line with the new last column
        return new_line
    
    def get_coref_info( self): # -> string
        """
        building the string to be added into the line
        """
        if ( not self.actual_coref_record.dropped ):
            string = "Coref=" # coreferent is represented in the surface layer
        elif ( self.actual_coref_record.dropped ):
            string = "Drop_coref=" # coreferent is dropped
        string += str( self.actual_coref_record.cluster_ID)
        return string
    
    def write_sentnce_id( self): # void
        """
        printing the paragraph and sentence ID as a head of the sentence - between the blank line and the first record line
        """
        self.conllu_output_coref.write( "#\t$\t" + str( self.para_ID) + "\t" + str( self.sent_ID) + "\n" )
        self.conllu_output_plain.write( "#\t$\t" + str( self.para_ID) + "\t" + str( self.sent_ID) + "\n" )
    
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