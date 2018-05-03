# auxiliary class for coreference transcription from onf files to conllu files
# representing one coreference cluster with lists of its members - at the beginning in the form of onto coreferents, later as udapi nodes

class Onto_cluster:
    def __init__( self):
        self.onto_coreferents = []
        self.node_coreferents = []
    def add_onto_coreferent( self, onto_coreferent):
        self.onto_coreferents.append( onto_coreferent)
    def set_node_coreferents( self, list_of_node_coreferents):
        self.node_coreferents = [ node_coreferent for node_coreferent in list_of_node_coreferents if node_coreferent != None ]
