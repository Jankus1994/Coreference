# Jan Faryad
#
# conversion of sentences fron onf file to plain text

class Onto_converter:
    def __init__( self, input_file_name, output_file_name):
        input_file = open( input_file_name, 'r')
        output_file = open( output_file_name, 'w')
        self.convert_file( input_file, output_file)
        input_file.close()
        output_file.close()
        
    def convert_file( self, input_file, output_file):
        converted = ""
        active = False # if we read the plain sentence
        for line in input_file:            
            if ( line == '\n'):
                active = False
            if ( active ):
                if ( line != "---------------\n"):                
                    converted += self.remove_punct_spaces( line[3:-1])
            elif ( "Coreference chains" in line ): # end of the section
                converted += "\n\n"
            elif ( "Plain sentence" in line ):
                active = True
        output_file.write( converted)

    def remove_punct_spaces( self, string): # -> string
        """ removing spaces before punctuation """
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
                

name = "a2e_0000"
#name = "ann_0001"    
#name = "ectb_1003"
#name = "abc_0001"

input_file_name = "/afs/ms.mff.cuni.cz/u/f/faryadj/udapi-python/demo/" + name + ".onf"
output_file_name = "/afs/ms.mff.cuni.cz/u/f/faryadj/udapi-python/demo/" + name + ".txt"
a = Onto_converter( input_file_name, output_file_name)
