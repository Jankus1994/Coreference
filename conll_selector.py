# Jan Faryad
# 27. 4. 2017
#
# selection of features for feature vectors

from conll_api import CoNLL_API as api

class CoNLL_selector:
    def __init__( self, document):
        self.document = document
    def process_document( self): # -> list of quadruplets ( Node, Node, list of features, bool)
        pairs_with_vectors = []
        for paragraph in api.get_paragraphs( self.document):
            for sentence in api.get_sentences( paragraph):
                for node in api.get_nodes( sentence): # linear cycle through all nodes in the document
                    if ( api.has_upostag( node, [ "PRON", "DET" ]) and # if we are suppose to detect coreference
                        api.has_feature( node, "PronType", [ "Prs", "Rel", "Dem" ]) ):
                        # !!! CONDITION FOR PRO-DROPS MISSING !!!
                        candidates = self.search_candidates( node) # list of candidates for coreference
                        for candidate in candidates:
                            feature_vector = self.build_feature_vector( node, candidate)
                            target_value = api.are_coreferents( node, candidate)
                            pairs_with_vectors.append( ( node, candidate, feature_vector, target_value ))
        return pairs_with_vectors
    
    def search_candidates( self, node): # -> list of Nodes
        """
        selects possible coreferents of the given node
        COULD BE CHANGED IN THE FUTURE
        """
        actual_sentence = api.get_sentence( node)
        previous_sentence = api.previous_sentence( actual_sentence)
        next_sentence = api.next_sentence( actual_sentence)
        
        candidates = self.search_sentence_for_candidates( node, actual_sentence)
        
        backwards_distance = 3 # 3 previous sentences
        for i in range( backwards_distance):
            if ( previous_sentence != None ):
                candidates += self.search_sentence_for_candidates( node, previous_sentence)
                previous_sentence = api.previous_sentence( previous_sentence)
                
        if ( next_sentence != None ):
            candidates += self.search_sentence_for_candidates( node, next_sentence)
        # ...PPPAN... we search three sentences backwards, the actual and the next sentence
        
        return candidates
    def search_sentence_for_candidates( self, node, sentence): # -> list of Nodes
        """
        candidates from the given setences
        """
        nodes = api.get_nodes( sentence)
        candidates = []
        for candidate in nodes:
            if ( self.consider_candidate( node, candidate) ):
                candidates.append( candidate)
        return candidates
    def consider_candidate( self, node, candidate): # -> bool
        """
        if "candidate" is an appropriate candidate for coreference with "node"
        COULD BE CHANGED IN THE FUTURE
        """
        if ( node == candidate ):
            return False
        if ( api.has_upostag( candidate, ["NOUN", "PRON", "VERB"]) ):
            return True
        return False
    def build_feature_vector( self, node, candidate): # -> list - feature vector for the given pair
        """
        for now, list of bools, but ints (distances) are also considerable
        !!! SHOULD BE CHANGED IN THE FUTURE !!!
        """
        feature_vector = []
        same_sentence = api.in_same_sentence( node, candidate)
        
        # distances
        # feature_vector.append( same_sentence)
        # if ( same_sentence ):
        #     feature_vector.append( True) # same paragraph
        #     feature_vector.append( api.surface_node_distance( node, candidate))
        # else:
        #     same_paragraph = api.in_same_paragraph( node, candidate)
        #     feature_vector.append( same_paragraph)
        #     if ( same_paragraph ):
        #         feature_vector.append( api.surface_sentence_distance( node, candidate))
        #     else:
        #         feature_vector.append( api.surface_paragraph_distance( node, candidate))
        # feature_vector.append( api.depth_distance( node, candidate))
        # feature_vector.append( api.compound_distance( node, candidate))
        # feature_vector.append( api.ccs_depth( node, candidate))

        anaphoric_pronoun = api.get_id( node) > api.get_id( candidate) # the pronoun is after its antecedent - anaphora
        feature_vector.append( same_sentence and anaphoric_pronoun)
        
        # grammar
        # ? not only bool for equality, but also categories ?
        feature_vector.append( api.has_feature( node, "Case", api.get_features_by_name( candidate, "Case"))) # same case
        feature_vector.append( api.has_feature( node, "Gender", api.get_features_by_name( candidate, "Gender"))) # same gender
        feature_vector.append( api.has_feature( node, "Number", api.get_features_by_name( candidate, "Number"))) # same number
        
        # pronoun
        feature_vector.append( api.has_feature( node, "PronType", ["Dem"])) # demonstrative
        feature_vector.append( api.has_feature( node, "PronType", ["Prs"])) # personal
        feature_vector.append( api.has_feature( node, "PronType", ["Rel"])) # relative
        feature_vector.append( api.has_feature( node, "Reflex", ["Yes"])) # reflexive
        feature_vector.append( api.has_feature( node, "Poss", ["Yes"])) # possessive
        
        # candidate
        # part of speech
        feature_vector.append( api.has_upostag( candidate, ["NOUN"]))
        feature_vector.append( api.has_upostag( candidate, ["PRON"]))
        feature_vector.append( api.has_upostag( candidate, ["VERB"]))
        # function in the sentence
        feature_vector.append( api.has_deprel( candidate, ["nsubj"])) # nominal subject
        
        return feature_vector    