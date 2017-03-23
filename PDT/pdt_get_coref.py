# PRI NEVYJADRENYCH ZAMENACH APISOVAT ID RIADIACEHO CLENU!

from auxiliaries import get_interstring

class PDT_get_coreference:    
    def __init__( self, pdt_t_input):#, pdt_w_input, conllu_input, conllu_output):
        self.pdt_t_input = pdt_t_input        
        #self.pdt_w_input = pdt_w_input
        #self.conllu_input = conllu_input
        #self.conllu_output = conllu_output
        
        self.list_of_corefs = []
        self.list_of_paragraphs = []
        self.list_of_dropped = [] # list of tuples[2] (dropped ID, parent ID); parent ~ closest non-dropped supernode
    def read_file( self):
        line = self.pdt_t_input.readline()
        while not ( "</trees" in line ):
            if ( "<LM id" in line ):
                line = self.read_node( line, "" )
            else:
                line = self.pdt_t_input.readline()
        return ( self.list_of_corefs )
        
    def read_node( self, first_line, supernode_ID): # -> string
        """
        processes a node in the tectogrammatical tree: lets process children recursively
        and controls if the node corefers with another node.
        stops if the node record ends (start pf a new node, end of children block, end of file)
        returns the line, where the cycle stopped, typicaly the line with ID of a new node
        
        first line : string - line with the node ID
        supernode_ID : list (int[3]) - ID of the parent (or the closest not dropped predecessor) in case this node is a t-node, dropped pronoun
        """
        ( actual_ID, type ) = self.read_infos( first_line)
        if ( type == "sentence" ): # sentence node, not word node
            para_ID = self.paragraph_ID( actual_ID)
            #print(first_line)
            self.add_sentence( para_ID)
        elif ( type == "dropped" ):
            self.add_dropped( actual_ID, supernode_ID)
            actual_ID = supernode_ID # if the pronoun is dropped, it will be identified by its parent
        actual_infos = ( actual_ID, type )
        
        line = self.pdt_t_input.readline()
        while not ( "<LM id" in line or "</children" in line or "</trees" in line ):            
        # reading upto the end of the node; children and coreferences and processed separately
        # controlling </LM> tag wouldn't work as there are inner <LM>...</LM> blocks
            if ( "<coref_gram" in line or "<coref_text" in line ): # not coref special
                coref_record = self.process_coref( line, actual_infos)
                #if ( not 'w' in coref_record.own_ID):
                #    print(first_line)
                if ( coref_record != None ):
                    self.list_of_corefs.append( coref_record)#self.insert_coref_record( coref_record)
            elif ( "<children" in line ):
                self.process_children( actual_ID)
            line = self.pdt_t_input.readline()
        return line
    
    def paragraph_ID( self, string):        
        last = string.split( '-')[-1]
        para_string = get_interstring( last, 'p', 's')
        return int( para_string)
    
    def add_dropped( self, dropped_ID, supernode_ID): # void
        self.list_of_dropped += [ ( dropped_ID, supernode_ID ) ]
    def get_dropped( self, dropped_ID): # -> string - supernode ID
        for i in self.list_of_dropped:
            if ( i[0] == dropped_ID ):
                return i[1]
        # returns None if the dropped word is a direct descendant of the sentence node
        
    #def insert_coref_record( self, coref_record):
     #   self.list_of_corefs.append( coref_record)
        """
        if ( len( self.list_of_corefs) == 0 ):
            self.list_of_corefs = [ coref_record ]
        else:            
            for i in range( len( self.list_of_corefs)):
                if ( self.list_of_corefs[i].own_ID > coref_record.own_ID):
                    self.list_of_corefs = self.list_of_corefs[:i] + [ coref_record ] + self.list_of_corefs[i:]
                    break
            else:
                self.list_of_corefs += [ coref_record ]
            """
    
    def add_sentence( self, para_ID): # void
        """
        increases the number of sentences in the given paragraph        
        """
        para_ID -= 1 # paragraphs are indexed from 1
        if ( len( self.list_of_paragraphs) > para_ID ): # increasing number of senteces in the last paragraph
            self.list_of_paragraphs[para_ID] += 1
        else: # a new paragraph
            for i in range( para_ID - len( self.list_of_paragraphs) ):
                self.list_of_paragraphs += [ 0 ]
            self.list_of_paragraphs += [ 1 ]
        #print(self.list_of_paragraphs)
                
    def read_infos( self, string):
        id_string = get_interstring( string, '"', '"')      
        type = self.ID_type( id_string)
        return ( id_string, type)
        
    def process_coref( self, first_line, actual_info): # -> Coreference_record
        """
        reads coreferent ID and creates a new coreference record
        """
        ( actual_ID, actual_type ) = actual_info
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

        coref_type = self.ID_type( coref_ID) # pair (bool, bool) : ( word(True)/sentence(False), is dropped )
        #actual_ID = actual_info[0]
        #actual_dropped = actual_info[1]
        
        if ( coref_type == "dropped" ): # replace a reference to dropped pronoun with a reference to its non-dropped supernode
            coref_ID = self.get_dropped( coref_ID)
            
        if ( actual_ID != None and coref_ID != None ):            
            record = Coreference_record( actual_type == "dropped", actual_ID, coref_type == "dropped", coref_ID)
            return record
        return None
        
    
    def ID_type( self, string): # -> pair (bool, bool)
        """
        recognizes if the node is a word node (T) or a sentence node (F)
        and if it is dropped
        """
        string = string.split( '-')[-1]        
        for char in string[::-1]: # reversed string
            #if ( char == 'w'):
            if ( 'w' in string):
                return "word"
            #elif ( char == 'a'):
            elif ( 'a' in string):
                return "dropped"
            #elif ( char == 's' or () ):
            elif ( 's' in string):
                return "sentence"            
            #elif ( char < '0' or char > '9' ):
            else:
                return "other"
        return "other"
        """
        id_string = string.split('-')[-1] # annotation_layer-text-file-id
        dropped = False
        number_string = ""
        para_ID = -1
        sent_ID = -1
        word_ID = -1
        for char in id_string[1:]: # 'p'
            if ( char == 's' ):
                para_ID = int( number_string)
                number_string = ""
            elif ( char == 'w' ):
                sent_ID = int( number_string)
                number_string = ""
            elif ( char == 'a' ): # for dropped words
                sent_ID = int( number_string)                
                number_string = ""
                dropped = True  #
            elif ( char >= '0' and char <= '9' ):
                number_string += char
        if ( sent_ID != -1):
            word_ID = int( number_string)
        else:
            sent_ID = int( number_string)
        return ( para_ID, sent_ID, word_ID, dropped )"""
        
    def process_children( self, supernode_ID):
        line = self.pdt_t_input.readline()
        while not ( "</children" in line ):
            if ( "<LM id" in line ):
                line = self.read_node( line, supernode_ID) # returned value is an id line of the next child or </children>
            else:
                line = pdt_t_input.readline() # there was sometging between </LM> and <LM id...>                
"""class ID_type(Enum):
    Word = 1
    Dropped = 2
    Sentence = 3
    Other = 4"""
class Coreference_record:    
    def __init__( self, own_dropped, own_ID, coref_dropped, coref_ID):
        self.own_dropped = own_dropped
        self.coref_dropped = coref_dropped
        # self.t_lemma
        self.own_ID = own_ID
        self.coref_ID = coref_ID
