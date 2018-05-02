# auxiliary class for coreference transcription from onf files to conllu files
# representing one corefering phrase (not only one word!) with its text and position in the text
# instances are elements of list of onto coreferents in their corresponding onto cluster

class Onto_coreferent:
    def __init__( self, position_string, form):
        self.position_string = position_string # string
        self.form = form # string, the coreferenting word

