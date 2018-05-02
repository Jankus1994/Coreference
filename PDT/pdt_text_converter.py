""" Extraction of plain text frm PDT .w file (in XML format) """

import sys
from udapi.block.demo.Coreference.Conv.conv import Conv_text_converter
from udapi.block.demo.Coreference.Other.auxiliaries import get_interstring

class Pdt_text_converter( Conv_text_converter):
    def convert_file( self, input_file, output_file):
        actual_word = ""
        new_word = False
        sent_id = None
        for line in input_file:        
            if ( "<w " in line ): # eg. <w id="w-cmpr9410-009-p3s1w1">
                new_word = True
                id_string = get_interstring( line, '"', '"') # eg. w-cmpr9410-009-p3s1w1
                word_id = id_string.split( '-')[-1] # eg. p3s1w1
                new_sent_id = get_interstring( word_id, 'p', 'w') # the paragraph number should be also a part of sent id, because if there were only one sentence in the paragraph, there would be two sentences with id "1" next to each other, but the paragraph number would differ
                if ( new_sent_id != sent_id ): # break line at new sentence - we need one sentence per line
                    if ( sent_id != None ): # except the first one
                        output_file.write( '\n')
                    sent_id = new_sent_id
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

if ( len( sys.argv) == 3 ):
    Pdt_text_converter( sys.argv[1], sys.argv[2])



