

class Onto_get_coreference:
    def __init__( self, onto_coref_input):
        self.onto_coref_input = onto_coref_input
        self.list_of_texts = []
    
    def read_file( self):        
        active_text = False
        active_chain = False
        for line in self.onto_coref_input:
            if ( "Coreference chains" in line ):
                active_text = True
                text_id = self.get_text_id( line)
                text = Onto_text( text_id)
                self.list_of_texts.append( text)
            elif ( "Plain sentence" in line ):
                active_text = False
            
            elif ( active_text and "(IDENT)" in line ):
                active_chain = True
                chain = Onto_chain()
                text.add_chain( chain) # surely exists
            elif ( active_text and line == '\n' ):
                active_chain = False
            
            elif ( active_chain ):
                processed = self.process_coref_line( line)
                if ( processed != None ):
                    ( position_string, first_word ) = processed
                    coreferent = Onto_coreferent( position_string, first_word)
                    chain.add_coref( coreferent)
    
    def get_text_id( self, line):
        last = line.split( ' ')[-1]
        number_string = last[:-2]
        return int( number_string)
                
    def process_coref_line( self, line): # -> ( string, string )
        line_list = line.split( ' ')
        if ( len( line_list) < 17 ):
            return None
        position = line_list[15]
        if ( position == "" ):
            return None
        first_word = "" # the coreference will be marked only for the first word of the phrase - typically this is the pronouns we are looking for
        for item in line_list[16:]:
            if ( item != "" ):
                first_word = item
                break
        if ( first_word[-1] == '\n' ):
            first_word = first_word[:-1]
        return ( position, first_word )

class Onto_coreferent:
    def __init__( self, position_string, form):
        self.position_string = position_string # string
        self.form = form # string, the coreferenting word
class Onto_chain:
    def __init__( self):
        self.corefs = []
    def add_coref( self, coref):
        self.corefs.append( coref)
class Onto_text:
    def __init__( self, text_id):
        self.text_id = text_id
        self.chains = []
    def add_chain( self, chain):
        self.chains.append( chain)
        
name = "cctv_0000"
input_file_name = "C:\Komodo\Projekty\\" + name + ".onf"
input_file = open( input_file_name, 'r')
a = Onto_get_coreference( input_file)
a.read_file()
for i in a.list_of_texts:
    print("---- " + str( i.text_id) + " ----")
    for j in i.chains:
        for k in j.corefs:
            print( k.position_string + ' ' + k.form)
        print("")
                
