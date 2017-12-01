# Jan Faryad
#
# a component for obtaining the information about coreference from pdt files

from udapi.block.demo.Coreference.Conv.conv import Conv_coreference_getter
from udapi.block.demo.Coreference.PDT.pdt_coreferent import Pdt_coreferent
from udapi.block.demo.Coreference.Other.auxiliaries import get_interstring
from enum import Enum

class Pdt_coreference_getter( Conv_coreference_getter):    
    def execute( self, filename): # -> list (of coreference records)
        """the main method, called from outside"""
        # initialization
        self.pdt_t_input = open( filename + ".t", 'r') # deep syntactical (tectogrammatical) layer      
        self.list_of_corefs = [] # elements will be instances of Pdt_coreferent
        self.list_of_paragraphs = [] # elements are ints: list_of_paragraphs[i] indicates the number of sentences in the i-th paragraph
        self.list_of_dropped = [] # list of tuples[2] (dropped ID, "parent" ID); "parent" ~ closest non-dropped supernode
        #
        
        line = self.pdt_t_input.readline()
        while not ( "</trees" in line ): # end of filen
            if ( "<LM id" in line ): # beginning of a node
                line = self.read_node( line, "" ) # process node, returns the next line after the node
            else:
                line = self.pdt_t_input.readline() # continue
        
        self.pdt_t_input.close()
        return ( self.list_of_corefs )
        
    def read_node( self, first_line, supernode_ID): # -> string
        """
        processes a node in the tectogrammatical tree: lets process children recursively
        and controls if the node corefers with another node.
        stops if the node record ends (start pf a new node, end of children block, end of file)
        returns the line, where the cycle stopped, typically the line with ID of a new node
        
        first line : string - line with the node ID
        supernode_ID : list (int[3]) - ID of the parent (or the closest non-dropped predecessor) in case this node is a t-node, dropped pronoun
        """
        ( actual_ID, type ) = self.read_infos( first_line) # information about the node, got from the first line
        if ( type == Node_type.Sentence ): # a sentence node, not a word node
            para_ID = self.get_paragraph_ID( actual_ID)
            self.add_sentence( para_ID) # increases number of senteces in the actual paragraph
        elif ( type == Node_type.Dropped ): # node of a dropped word
            self.add_dropped( actual_ID, supernode_ID) # adding this tuple to the list of dropped nodes
            actual_ID = supernode_ID # if the pronoun is dropped, it will be identified by its parent
        actual_infos = ( actual_ID, type )
        
        line = self.pdt_t_input.readline()
        while not ( "<LM id" in line or "</children" in line or "</trees" in line ):            
        # reading upto the end of the node; children and coreferences and processed separately
        # controlling </LM> tag wouldn't work as there are inner <LM>...</LM> blocks
            if ( "<coref_gram" in line or "<coref_text" in line ): # not coref_special
                coref_record = self.process_coref( line, actual_infos)
                if ( coref_record != None ):
                    self.list_of_corefs.append( coref_record)
            elif ( "<children" in line ):
                self.process_children( actual_ID) # recursively process chilren nodes
            line = self.pdt_t_input.readline()
        return line
    
    def get_paragraph_ID( self, id_string): # -> int
        """
        gets the number of the actual paragraph from the id of the actual node
        id_string ... of a sentence, e.g. t-lnd94103-052-p1s11
        """
        last = id_string.split( '-')[-1]
        id = get_interstring( last, 'p', 's')
        return int( id)
    
    def add_dropped( self, dropped_ID, supernode_ID): # void
        """
        adding a pair (id of dropped node, id of its parent) to the list of drooped nodes
        """
        self.list_of_dropped += [ ( dropped_ID, supernode_ID ) ]
    def get_dropped( self, dropped_ID): # -> string - supernode ID
        """
        for the id of a dropped node returns its parent's id
        returns None if the dropped word is a direct descendant of the sentence node
        """
        for i in self.list_of_dropped:
            if ( i[0] == dropped_ID ):
                return i[1]
    
    def add_sentence( self, para_ID): # void
        """
        increases the number of sentences in the given paragraph        
        """
        para_ID -= 1 # paragraphs are indexed from 1, elements of the list from 0
        if ( len( self.list_of_paragraphs) > para_ID ): # increasing number of senteces in the last paragraph
            self.list_of_paragraphs[para_ID] += 1
        else: # a new paragraph
            for i in range( para_ID - len( self.list_of_paragraphs) ):
                self.list_of_paragraphs += [ 0 ] # leaping over empty paragraphs - there are in some texts
            self.list_of_paragraphs += [ 1 ] # the actual, new paragraph with its first sentence marked
                
    def read_infos( self, first_line): # -> (string, Node_type) 
        """
        obtains information about a node from its first line
        return a pair of id string (substring of the first line containing node id) and enum        
        """
        id_string = get_interstring( first_line, '"', '"') # gots substring between first two quotes   
        type = self.get_node_type( id_string) # recognizes node type
        return ( id_string, type)
        
    def process_coref( self, first_line, actual_info): # -> Pdt_coreferent
        """
        reads coreferent ID and creates a new coreference record        
        """
        ( actual_ID, actual_type ) = actual_info # id_string and Node_type (word or dropped)
        coref_ID = ""
        if ( "<coref_gram" in first_line ):
            line = self.pdt_t_input.readline()
            coref_ID = get_interstring( line, '>', '<')
        elif ( "<coref_text" in first_line ):
            self.pdt_t_input.readline() # <LM>
            line = self.pdt_t_input.readline()
            coref_ID = get_interstring( line, '>', '<')
        #elif ( "<coref_special" in first_line ):
        #    pass # segments or exophorae - they don't refere to any word in file

        coref_type = self.get_node_type( coref_ID) # 
        
        if ( coref_type == Node_type.Dropped ): # replace a reference to dropped pronoun with a reference to its non-dropped supernode
            coref_ID = self.get_dropped( coref_ID)
            
        if ( actual_ID != None and coref_ID != None ):   # creating a new coreference record          
            record = Pdt_coreferent( actual_type == Node_type.Dropped, actual_ID, coref_type == Node_type.Dropped, coref_ID)
            return record
        
    
    def get_node_type( self, id_string): # -> Node_type (enum)
        """
        recognizes if the node is a word node, t-node (dropped) or a sentence node
        """
        id = id_string.split( '-')[-1] # eg. t-lnd94103-052-p1s10w5, where t-lnd94103-052 is id of the file in the trebank,
                                        # p1s10w5 is id of the node (1st paragraph, 10th sentence, 5th word)
        if ( 'w' in id): # p1s10w5
            return Node_type.Word
        elif ( 'a' in id): # p1s10a5
            return Node_type.Dropped
        elif ( 's' in id): # p1s10
            return Node_type.Sentence
        return Node_type.Other # l28A ... ?!
        
    def process_children( self, supernode_ID): # void
        """
        processes children nodes of some node
        supernode id - id of o parent of these children or, in case it's dropped, of the first non-dropped predecessor
        """
        line = self.pdt_t_input.readline()
        while not ( "</children" in line ):
            if ( "<LM id" in line ):
                line = self.read_node( line, supernode_ID) # returned value is an id line of the next child or </children>
            else:
                line = pdt_t_input.readline() # there was something between </LM> and <LM id...>, typically, there's nothing   

class Node_type( Enum):
    Word = 1
    Dropped = 2
    Sentence = 3
    Other = 4
