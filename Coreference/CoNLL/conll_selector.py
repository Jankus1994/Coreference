# Jan Faryad
# 27. 4. 2017
#
# selection of features for feature vectors

from udapi.core.block import Block

class Conll_selector( Block):
    def process_node( self, node):
        if ( self.has_upostag( node, [ "PRON", "DET" ]) and # if we are suppose to detect coreference
            self.has_feature( node, "PronType", [ "Prs", "Rel", "Dem" ]) ):
            # !!! CONDITION FOR PRO-DROPS MISSING !!!
            self.search_candidates( node) # list of candidates for coreference
    
    def search_candidates( self, node): # void
        """
        selects possible coreferents of the given node
        COULD BE CHANGED IN THE FUTURE
        """
        actual_bundle = self.get_bundle( node)
        previous_bundle = self.previous_bundle( actual_bundle)
        next_bundle = self.next_bundle( actual_bundle)
        
        self.search_bundle_for_candidates( node, actual_bundle)
        
        backwards_distance = 3 # 3 previous sentences
        for i in range( backwards_distance):
            if ( previous_bundle != None ):
                #candidates += self.search_bundle_for_candidates( node, previous_bundle)
                self.search_bundle_for_candidates( node, previous_bundle)
                previous_bundle = self.previous_bundle( previous_bundle)
                
        if ( next_bundle != None ):
            #candidates += self.search_sentence_for_candidates( node, next_sentence)
            self.search_bundle_for_candidates( node, next_bundle)
        # ...PPPAN... we search three sentences backwards, the actual and the next sentence
        
    def search_bundle_for_candidates( self, node, bundle): # void
        """
        candidates from the given setences
        """
        root = bundle.trees[0]
        for candidate in root.descendants:
            if ( self.consider_candidate( node, candidate) ):
                #candidates.append( candidate)
                self.print_feature_vector( node, candidate)
        #return candidates
    def consider_candidate( self, node, candidate): # -> bool
        """
        if "candidate" is an appropriate candidate for coreference with "node"
        COULD BE CHANGED IN THE FUTURE
        """
        if ( node == candidate ):
            return False
        if ( self.has_upostag( candidate, ["NOUN", "PRON", "VERB"]) ):
            return True
        return False
    def print_feature_vector( self, node, candidate): # void
        """
        for now, list of bools, but ints (distances) are also considerable
        !!! SHOULD BE CHANGED IN THE FUTURE !!!
        """
        feature_vector = []
        node_bundle = self.get_bundle( node)
        candidate_bundle = self.get_bundle( candidate)
        same_sentence = ( node_bundle == candidate_bundle )
        
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

        anaphoric_pronoun = node.ord > candidate.ord # the pronoun is after its antecedent - anaphora
        feature_vector.append( same_sentence and anaphoric_pronoun)
        
        # grammar
        # ? not only bool for equality, but also categories ?
        feature_vector.append( self.has_feature( node, "Case", candidate.feats['Case'].split( ','))) # same case
        feature_vector.append( self.has_feature( node, "Gender", candidate.feats['Gender'].split( ','))) # same gender
        feature_vector.append( self.has_feature( node, "Number", candidate.feats['Number'].split( ','))) # same number
        
        # pronoun
        feature_vector.append( self.has_feature( node, "PronType", ["Dem"])) # demonstrative
        feature_vector.append( self.has_feature( node, "PronType", ["Prs"])) # personal
        feature_vector.append( self.has_feature( node, "PronType", ["Rel"])) # relative
        feature_vector.append( self.has_feature( node, "Reflex", ["Yes"])) # reflexive
        feature_vector.append( self.has_feature( node, "Poss", ["Yes"])) # possessive
        
        # candidate
        # part of speech
        feature_vector.append( candidate.upos == "NOUN" )
        feature_vector.append( candidate.upos == "PRON" )
        feature_vector.append( candidate.upos == "VERB" )
        # function in the sentence
        feature_vector.append( candidate.udeprel == "nsubj" ) # nominal subject
        
        # target_value
        if ( self.for_training() ):
            feature_vector.append( self.are_coreferents( node, candidate))
        
        feature_vector.append(node.form)        
        feature_vector.append(candidate.form)
        
        feature_vector.append(node_bundle.bundle_id)
        feature_vector.append(node.ord)
        
        feature_vector.append(candidate_bundle.bundle_id)
        feature_vector.append(candidate.ord)
        
        for i in range( len( feature_vector) - 1):
            print( feature_vector[i], end='\t')
        print( feature_vector[-1])
    
    def for_training( self):
        return True
    
    ## ## ## complementary interface
    
    def has_upostag( self, node, list_of_possible_upostags): # -> bool
        """
        controls if the node's upostag is on of the possible ones
        """
        return ( node.upos in list_of_possible_upostags )
    
    def has_feature( self, node, feature_name, list_of_possible_values): # -> bool
        """
        controls if the node has the given feature and if one of it's values is possible
        """
        list_of_real_values = node.feats[ feature_name ].split( ',')
        return ( len( set( list_of_real_values) & set( list_of_possible_values) ) > 0 )
    def get_bundle( self, node):
        n = node
        while ( not n.is_root() ):
            n = n.parent
        return n.bundle
    def previous_bundle( self, bundle):
        bundle_id = int( bundle.bundle_id)
        if ( bundle_id > 1 ):
            doc = bundle.document()
            return doc.bundles[ bundle_id - 2 ] # bundles are indexed from 1, lists from 0  
    def next_bundle( self, bundle):
        bundle_id = int( bundle.bundle_id)
        doc = bundle.document()
        if ( bundle_id < len( doc.bundles) ):
            return doc.bundles[ bundle_id ] # bundles are indexed from 1, lists from 0    
    def are_coreferents( self, node, candidate): # -> bool
        """
        if two nodes are in the same coreference cluster
        """
        coref_1 = node.misc['Coref']
        drop_coref_1 = node.misc['Drop_coref']
        coref_2 = candidate.misc['Coref']
        drop_coref_2 = candidate.misc['Drop_coref']
        for c in [ coref_1, drop_coref_1 ]:
            if ( c != "" and c in [ coref_2, drop_coref_2 ] ):                
                return True
        return False        
    
