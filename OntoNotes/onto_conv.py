class Onto_converter:
    def __init__( self, input_file_name, output_file_name):
        input_file = open( input_file_name, 'r')
        output_file = open( output_file_name, 'w')
        self.convert_file( input_file, output_file)
        input_file.close()
        output_file.close()
        
    def convert_file( self, input_file, output_file):
        converted = ""
        active = False
        for line in input_file:            
            if ( line == '\n'):
                active = False
            if ( active ):
                if ( line != "---------------\n"):                    
                    converted += self.remove_punct_spaces( line[3:-1])
            elif ( "Coreference chains" in line ):
                converted += "\n\n"
            elif ( "Plain sentence" in line ):
                active = True
        print("yu")
        output_file.write( converted)
        """
            new_line = ""
            active = True
            for char in line:
                if ( char == '<' ):
                    active = False                
                if ( active ):
                    new_line += char
                if ( char == '>' ):
                    active = True
            print( new_line)
            """
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
                
    
name = "cctv_0000"
#name = "abc_0001"

input_file_name = "C:\Komodo\Projekty\\" + name + ".onf"
output_file_name = "C:\Komodo\Projekty\\" + name + ".txt"
a = Onto_converter( input_file_name, output_file_name)
