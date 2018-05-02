# Jan Faryad
# 19. 6. 2017

"""Main class for transcription of coreference information from PDT files (.w and . t) to CoNLL-U"""

from udapi.block.demo.Coreference.Conv.conv import Conv_coref
from udapi.block.demo.Coreference.PDT.pdt_word_correspondence import Pdt_word_correspondence
from udapi.block.demo.Coreference.PDT.pdt_coreference_getter import Pdt_coreference_getter
from udapi.block.demo.Coreference.PDT.pdt_word_converter import Pdt_word_converter
from udapi.block.demo.Coreference.PDT.pdt_coreference_setter import Pdt_coreference_setter


class Pdt_coref_conversion( Conv_coref):
    def __init__( self):
        super().__init__()
        self.word_correspondence  = Pdt_word_correspondence()
        self.coreference_getter   = Pdt_coreference_getter()
        self.word_converter       = Pdt_word_converter()
        self.coreference_setter   = Pdt_coreference_setter()    
