# Jan Faryad
# 18. 11. 2017
#

from udapi.block.demo.Coreference.CoNLL.conll_rel_selector import Conll_rel_selector

class Conll_rel_prediction_selector( Conll_rel_selector):
    def for_training( self):
        return False
