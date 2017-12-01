import sys

from udapi.block.demo.Coreference.Conv.conv import Conv_text_converter
from udapi.block.demo.Coreference.Other.auxiliaries import get_interstring

class Pdt_text_converter( Conv_text_converter):
    def convert_file( self, input_file, output_file):
        text = ""
        actual_word = ""
        new_para = False
        new_word = False
        for line in input_file:
            if ( "</para>" in line ):
                new_para = True
            elif ( "<para>" in line and new_para ):
                output_file.write( '\n')
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

# name of the file
#name = "cmpr9410_001" # train 1
#name = "lnd94103_052" # train 8
#name = "ln94206_32" # train 5
#name = "cmpr9410_032" # train 2
#name = "ln94204_7" # train 2
#name = "mf930713_046" # train 2
#name = "ln94210_105" # train 2
#name = "ln95048_134" # train 3
#name = "mf920922_131" # train 7
#name = "mf930713_085" # train 1
#name = "mf930713_118" # train 3
#name = "ln95048_117" # train 6
#name = "ln94206_62" # train 8

#input_file_name = path + name + ".w"
#output_file_name = path + name + ".txt"

if ( len( sys.argv) == 3 ):
    c = Pdt_text_converter( sys.argv[1], sys.argv[2])



