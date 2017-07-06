# Jan Faryad
# 29. 6. 2017
#
# main class for processing OntoNotes files
# to be repaired:
#     path and file name won't be written in the code, will be extracted from document - changes in udapi needed

from udapi.core.block import Block
from udapi.block.demo.Coreference.OntoNotes.onto_word_correspondence import Onto_word_correspondence
from udapi.block.demo.Coreference.OntoNotes.onto_coreference_getter import Onto_coreference_getter
from udapi.block.demo.Coreference.OntoNotes.onto_word_conversion import Onto_word_conversion
from udapi.block.demo.Coreference.OntoNotes.onto_coreference_adder import Onto_coreference_adder


class Onto_main( Block):
    def process_document( self, document):
        
        path = "../demo/" # the actual folder is udapi-python/udapi
        
        # name of the file
        #name = "ectb_1003" #   
        #name = "ann_0001" # arabic
        #name = "a2e_0000"
        name = document.filename[:-10] # .in.conllu
        init_cluster_id = document.init_cluster_id    
        
        # building a matching between words in OntoNotes and CoNLL-U files
        onto_input = open( path+"../demo/" + name + ".onf", 'r')        
        word_correspondence = Onto_word_correspondence( onto_input, document)
        list_of_corresponding_words = word_correspondence.create_correspondence()
        onto_input.close()

        # extracting information about coreference from onf file
        onto_input = open( path + name + ".onf", 'r')
        coreference_getter = Onto_coreference_getter( onto_input)
        list_of_clusters = coreference_getter.process_file()
        onto_input.close()                

        # conversion of the onto IDs to udapi nodes
        Onto_word_conversion( list_of_clusters, list_of_corresponding_words) # void, conversion is made internally in the clusters (nodes are put into them)

        # adding the coreference information into the CoNLL-U file
        coref_adder = Onto_coreference_adder( list_of_clusters, init_cluster_id) # void, changes are made in the nodes (which are in the clusters)
        return coref_adder.cluster_id
