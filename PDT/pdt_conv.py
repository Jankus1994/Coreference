from auxiliaries import get_interstring

class PDT_converter:
    def __init__( self, input_file_name, output_file_name):
        input_file = open( input_file_name, 'r')
        output_file = open( output_file_name, 'w')
        self.convert_file( input_file, output_file)
        input_file.close()
        output_file.close()
        
    def convert_file( self, input_file, output_file):
        text = ""
        actual_word = ""
        new_para = False
        new_word = False
        for line in input_file:
            
            if ( "</para>" in line ):
                new_para = True
            elif ( "<para>" in line and new_para ):
                output_file.write( '\n\n')
                new_para = False
            
            elif ( "<w " in line ):
                new_word = True
            elif ( "</w>" in line and new_word ):
                output_file.write( actual_word)
                actual_word = ""
                new_word = False
            
            elif ( "<token>" in line ):
                token = get_interstring( line, '>', '<') + " "
                actual_word += token
            elif ( "<no_space_after>" in line ):
                value = get_interstring( line, '>', '<')
                if ( value == "1" ):
                    actual_word = actual_word[:-1]
        output_file.write( text)       

name = "ln94206_32"
input_file_name = "C:\Komodo\Projekty\\" + name + ".w"
output_file_name = "C:\Komodo\Projekty\\" + name + ".txt"
a = PDT_converter( input_file_name, output_file_name)
