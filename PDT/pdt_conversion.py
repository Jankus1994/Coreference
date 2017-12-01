# Jan Faryad
# 19. 6. 2017

from udapi.block.demo.Coreference.Conv.conv import Conv_main
from udapi.block.demo.Coreference.PDT.pdt_word_correspondence import Pdt_word_correspondence
from udapi.block.demo.Coreference.PDT.pdt_coreference_getter import Pdt_coreference_getter
from udapi.block.demo.Coreference.PDT.pdt_word_converter import Pdt_word_converter
from udapi.block.demo.Coreference.PDT.pdt_coreference_setter import Pdt_coreference_setter


class Pdt_conversion( Conv_main):
    def __init__( self):
        super( Pdt_conversion, self).__init__()
        self.word_correspondence  = Pdt_word_correspondence()
        self.coreference_getter   = Pdt_coreference_getter()
        self.word_converter       = Pdt_word_converter()
        self.coreference_setter    = Pdt_coreference_setter()    

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
