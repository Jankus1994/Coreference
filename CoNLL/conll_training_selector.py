# Jan Faryad
# 4. 7. 2017
#
# selector for training - idetical wit selector

from udapi.block.demo.Coreference.CoNLL.conll_selector import Conll_selector

class Conll_training_selector( Conll_selector):
    def for_training( self):
        return True
