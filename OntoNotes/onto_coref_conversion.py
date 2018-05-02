# Jan Faryad
# 29. 6. 2017
#
# main class for processing OntoNotes files
# to be repaired:
#     path and file name won't be written in the code, will be extracted from document - changes in udapi needed

from udapi.block.demo.Coreference.Conv.conv import Conv_coref
from udapi.block.demo.Coreference.OntoNotes.onto_word_correspondence import Onto_word_correspondence
from udapi.block.demo.Coreference.OntoNotes.onto_coreference_getter import Onto_coreference_getter
from udapi.block.demo.Coreference.OntoNotes.onto_word_converter import Onto_word_converter
from udapi.block.demo.Coreference.OntoNotes.onto_coreference_setter import Onto_coreference_setter


class Onto_coref_conversion( Conv_coref):
    def __init__( self):
        super().__init__()
        self.word_correspondence  = Onto_word_correspondence()
        self.coreference_getter   = Onto_coreference_getter()
        self.word_converter       = Onto_word_converter()
        self.coreference_setter   = Onto_coreference_setter()    
