# Jan Faryad
# 17. 11. 2017

""" inhereted feature printer for demonstrative pronouns """

from udapi.block.demo.Coreference.CoNLL.conll_feature_printer import Conll_feature_printer
from udapi.block.demo.Coreference.CoNLL.conll_specific_selectors import Conll_dem_training_selector

class Conll_dem_feature_printer( Conll_feature_printer):
    def __init__( self, **kwargs):
        super().__init__( **kwargs)
        self.selector = Conll_dem_training_selector()
