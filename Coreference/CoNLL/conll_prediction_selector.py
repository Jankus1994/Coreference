# Jan Faryad
# 4. 7. 2017
#
# selector for prediction - idetical wit selector

from udapi.block.demo.Coreference.CoNLL.conll_selector import Conll_selector

class Conll_prediction_selector( Conll_selector):
    def for_training( self):
        return False
