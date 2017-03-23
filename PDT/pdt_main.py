# Jan Faryad
# 19. 12. 2016
#
# main programm that runs four parts of adding the coreference information from PDT to CoNLL-U

from pdt_get_coref_II import *
from pdt_word_correspondence import PDT_word_correspondence
from pdt_id_conversion import PDT_ID_conversion
from pdt_add_coref_II import PDT_add_coreference

def listing( list_of_corefs): # void
    """
    prints attributes of coreference record in the give list
    """
    for i in list_of_corefs:
        print( ( i.own_dropped, i.own_ID, i.coref_dropped, i.coref_ID) )

name = "cmpr9410_001" # name of the file

# building a matching between words in PDT and CoNLL-U files
pdt_w_input = open( "C:\Komodo\Projekty\\"+name+".w", 'r', encoding="utf8") # surface (word) layer
conllu_input = open( "C:\Komodo\Projekty\\"+name+".in.conll", 'r', encoding="utf8")
word_correspondence = PDT_word_correspondence( pdt_w_input, conllu_input)
( list_of_corresponding_IDs, list_of_sentence_IDs ) = word_correspondence.create_correspondence()
conllu_input.close()
pdt_w_input.close()

# extracting information about coreference from
pdt_t_input = open( "C:\Komodo\Projekty\\"+name+".t", 'r', encoding="utf8") # deep syntactical (tectogrammatical) layer
get_coreference = PDT_get_coreference( pdt_t_input)
list_of_corefs_I = get_coreference.read_file()
pdt_t_input.close()

# conversion of the PDT IDs to CoNLL-U IDs
id_conversion = PDT_ID_conversion( list_of_corefs_I, list_of_corresponding_IDs)
list_of_corefs_II = id_conversion.convert_IDs()

# adding the coreference information into the CoNLL-U file
conllu_input = open( "C:\Komodo\Projekty\\"+name+".in.conll", 'r', encoding="utf8")
conllu_output = open( "C:\Komodo\Projekty\\"+name+".out.conll", 'w', encoding="utf8")
b = PDT_add_coreference( list_of_corefs_II, list_of_sentence_IDs, conllu_input, conllu_output)
b.process_file()
conllu_input.close()
conllu_output.close()
