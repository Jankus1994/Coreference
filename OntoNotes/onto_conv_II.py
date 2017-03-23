class Onto_converter:
    def __init__( self, input_file_name, output_file_name):
        input_file = open( input_file_name, 'r')
        output_file = open( output_file_name, 'w')
        self.convert_file( input_file, output_file)
        input_file.close()
        output_file.close()
        
        this.onto_sentences = []
        
    def convert_file( self, input_file, output_file):
        converted = ""
        active = False
        sentence = Onto_sentence()
        
        for line in input_file:
            if ()
            if ( active and line[4] >= '0' and line[4] <= '9' ):
                index = self.get_word_index( line[4:])
                word = Onto_word( index)
                sentence.add_word( word)
                
            if ( "Leaves:\n" == line ):
                active = True
            
    def remove_punct_spaces( self, string): # -> string
        if ( len( string) < 2 ):
            return string
        new_string = ""
        char_a = string[0]
        for char_b in string[1:]:
            if not ( char_a == ' ' and char_b in ".,?!:;'-\"" ):
                new_string += char_a
            char_a = char_b
        new_string += string[-1]
        return new_string
    
class Onto_word:
    def __init__( self, word_id):
        self.word_id = word_id
        
class Onto_sentence:
    def __init__( self):
        self.words = []
    def set_id( self, para_id, sent_id):
        self.para_id = para_id
        self.sent_id = sent_id
    def add_word( self, word):
        self.words.append( word)
                
    
name = "cctv_0000"
input_file_name = "C:\Komodo\Projekty\\" + name + ".onf"
output_file_name = "C:\Komodo\Projekty\\" + name + ".txt"
a = Onto_converter( input_file_name, output_file_name)
