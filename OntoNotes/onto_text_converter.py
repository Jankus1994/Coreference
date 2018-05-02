# Jan Faryad
#
# conversion of sentences fron an onf file to plain text

import sys

from udapi.block.demo.Coreference.Conv.conv import Conv_text_converter

class Onto_text_converter( Conv_text_converter):
    def convert_file( self, input_file, output_file):
        converted = ""
        active = False # if we are reading the plain text of a sentence sentence
        # the record of a plain sentence has the following form:
        
        # Plain sentence:
        # ---------------
        #     Mahmoud Mahmoud Al Belehi, the owner of a house close to the fire, confirms that the house was cracked when a charge of
        #     bottles entered the house and a fire started in it, cracking the ceiling and walls.
        
        for line in input_file:
            if ( "Plain sentence" in line ): # new sentence
                active = True
            elif ( line == '\n' and active ): # end of the sentence
                active = False
                converted += '\n' # we need one sentence per line                
            elif ( line != "---------------\n" and active ): # reading the text
                converted += line[4:-1] + ' ' # starting from the fifth column, it may continue on the next line, so we add a space insted of newline and don't deactivate reading sentence
        output_file.write( converted)
                
if ( len( sys.argv) == 3 ):
    Onto_text_converter( sys.argv[1], sys.argv[2])
