# Jan Faryad
# 19. 6. 2017

from udapi.core.block import Block
from udapi.block.demo.Coreference.PDT.pdt_word_correspondence import PDT_word_correspondence
from udapi.block.demo.Coreference.PDT.pdt_get_coreference import PDT_get_coreference
from udapi.block.demo.Coreference.PDT.pdt_id_conversion import PDT_ID_conversion
from udapi.block.demo.Coreference.PDT.pdt_clusterization import PDT_clusterization
from udapi.block.demo.Coreference.PDT.pdt_add_coreference import PDT_add_coreference


class Pdt_main( Block):
    def process_document( self, document):
        
        path = "../demo/" # the actual folder is udapi-python/udapi
        
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
        name = document.filename[:-9] # .in.conll       
        init_cluster_id = document.init_cluster_id        
        
        # building a matching between words in PDT and CoNLL-U files
        pdt_w_input = open( path + name + ".w", 'r') # surface (word) layer
        word_correspondence = PDT_word_correspondence( pdt_w_input, document)
        ( list_of_corresponding_IDs, list_of_sentence_IDs ) = word_correspondence.create_correspondence()
        pdt_w_input.close()

        # extracting information about coreference from
        pdt_t_input = open( path + name + ".t", 'r') # deep syntactical (tectogrammatical) layer
        get_coreference = PDT_get_coreference( pdt_t_input)
        list_of_corefs_I = get_coreference.read_file()
        pdt_t_input.close()

        # conversion of the PDT IDs to CoNLL-U IDs
        id_conversion = PDT_ID_conversion( list_of_corefs_I, list_of_corresponding_IDs)
        list_of_corefs_II = id_conversion.convert_IDs()

        # clusterization?? - conversion from chains to clusters
        clusterizer = PDT_clusterization( list_of_corefs_II, init_cluster_id)
        list_of_corefs_II = clusterizer.convert_chains_to_clusters()
        

        # adding the coreference information into the CoNLL-U file
        #listing(list_of_corefs_II)        
        #for i in list_of_corresponding_IDs:
        #    print(i)
        cored_adder = PDT_add_coreference( list_of_corefs_II, list_of_sentence_IDs, document)
        cored_adder.process_file()
        
        #document.store_conllu("modifik.conllu")
        return clusterizer.cluster_id
        
def listing( list_of_corefs): # void
    """
    prints attributes of coreference record in the given list
    """
    for i in list_of_corefs:
        print( ( i.para_ID, i.sent_ID, i.word_ID, i.cluster_ID, i.dropped) )        
