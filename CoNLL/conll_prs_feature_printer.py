# Jan Faryad
# 17. 11. 2017

""" inhereted feature printer for personal pronouns """

from udapi.block.demo.Coreference.CoNLL.conll_feature_printer import Conll_feature_printer
from udapi.block.demo.Coreference.CoNLL.conll_specific_selectors import Conll_prs_training_selector

class Conll_prs_feature_printer( Conll_feature_printer):
    def __init__( self, **kwargs):
        super().__init__( **kwargs)
        self.selector = Conll_prs_training_selector()
