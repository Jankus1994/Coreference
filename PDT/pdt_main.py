# Jan Faryad
# 19. 12. 2016
#
# main programm that runs several parts of adding the coreference information from PDT to CoNLL-U

from pdt_get_coref import *
#from pdt_get_coref_II import *
from pdt_word_correspondence import PDT_word_correspondence
from pdt_id_conversion import PDT_ID_conversion
#from pdt_add_coref import PDT_add_coreference
#from pdt_add_coref_II import PDT_add_coreference

# for version with the cluster-approach insted of chain-approach
from pdt_clusterization import *
from pdt_add_coref_cluster import PDT_add_coreference
#

def listing( list_of_corefs): # void
    """
    prints attributes of coreference record in the given list
    """
    for i in list_of_corefs:
        print( ( i.own_dropped, i.own_ID, i.coref_dropped, i.coref_ID) )

# name of the file
#name = "cmpr9410_001" # train 1
name = "lnd94103_052" # train 8
#name = "ln94206_32" # train 5
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

# clusterization?? - conversion from chains to clusters
clusterizer = PDT_clusterization( list_of_corefs_II)
list_of_corefs_II = clusterizer.convert_chains_to_clusters()

# adding the coreference information into the CoNLL-U file
conllu_input = open( "C:\Komodo\Projekty\\"+name+".in.conll", 'r', encoding="utf8")
conllu_output = open( "C:\Komodo\Projekty\\"+name+".out.conll", 'w', encoding="utf8")
b = PDT_add_coreference( list_of_corefs_II, list_of_sentence_IDs, conllu_input, conllu_output)
b.process_file()
conllu_input.close()
conllu_output.close()