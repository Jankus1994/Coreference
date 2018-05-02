# Jan Faryad
# 22. 3. 2018

""" inhereted feature printer for dropped personal pronouns """

from udapi.block.demo.Coreference.CoNLL.conll_feature_printer import Conll_feature_printer
from udapi.block.demo.Coreference.CoNLL.conll_specific_selectors import Conll_prodrop_training_selector

class Conll_prodrop_feature_printer( Conll_feature_printer):
    def __init__( self, **kwargs):
        super().__init__( **kwargs)
        self.selector = Conll_prodrop_training_selector()
