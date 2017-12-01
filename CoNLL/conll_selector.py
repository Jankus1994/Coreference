# Jan Faryad
# 27. 4. 2017
#
# selection of features for feature vectors

import math

class Conll_selector():    
    def process_node( self, node):
        self.feature_vectors = []
        if ( self.has_upostag( node, [ "PRON", "DET" ]) and # if we are suppose to detect coreference
            self.has_feature( node, "PronType", [ "Prs", "Rel", "Dem" ]) ):            
            self.search_candidates( node)
        
        if ( self.verb_without_subject( node) ):
            self.search_candidates( node)
        return self.feature_vectors
        
    
    def verb_without_subject( self, node):
        if ( not self.has_upostag( node, [ "VERB" ]) ): # not a verb
            return False
        for child in node.children:
            if ( self.has_deprel( node, [ "nsubj", "csubj" ]) ): # has a subject
                return False
        return True
    
    def search_candidates( self, node): # void
        """
        selects possible coreferents of the given node
        COULD BE CHANGED IN THE FUTURE
        """        
        actual_bundle = self.get_bundle( self.get_root_path( node))
        previous_bundle = self.previous_bundle( actual_bundle)
        next_bundle = self.next_bundle( actual_bundle)
        
        self.search_bundle_for_candidates( node, actual_bundle)
        
        backwards_distance = 3 # 1 previous sentence
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
        if ( self.has_upostag( candidate, [ "NOUN", "PRON", "VERB" ]) ):
            if ( self.has_feature( node, "Case", candidate.feats['Case'].split( ',')) ):
                return True
            if ( self.has_feature( node, "Gender", candidate.feats['Gender'].split( ',')) ):
                return True
            if ( self.has_feature( node, "Number", candidate.feats['Number'].split( ',')) ):
                return True          
        return False
    def print_feature_vector( self, node, candidate): # void
        """
        for now, list of bools, but ints (distances) are also considerable
        !!! SHOULD BE CHANGED IN THE FUTURE !!!
        """
        feature_vector = []
        node_root_path = self.get_root_path( node)
        candidate_root_path = self.get_root_path( candidate)
        node_bundle = self.get_bundle( node_root_path)
        candidate_bundle = self.get_bundle( candidate_root_path)
        same_sentence = ( node_bundle == candidate_bundle )
        
        # distances
        feature_vector.append( same_sentence)
        if ( same_sentence ):
            feature_vector.append( int( math.fabs( node.ord - candidate.ord)))
        else:
            feature_vector.append( int( math.fabs( int( node_bundle.bundle_id) - int( candidate_bundle.bundle_id))))
        
        node_depth = self.get_depth( node_root_path)
        candidate_depth = self.get_depth( candidate_root_path)
        feature_vector.append( node_depth)
        feature_vector.append( candidate_depth)
        feature_vector.append( int( math.fabs( node_depth - candidate_depth)))
        ccs_depth = self.get_ccs_depth( node_root_path, candidate_root_path)
        feature_vector.append( ccs_depth)
        feature_vector.append( int( math.fabs( node_depth - ccs_depth)) + int( math.fabs( ccs_depth - candidate_depth))) # compound distance

        anaphoric_pronoun = node.ord > candidate.ord # the pronoun is after its antecedent - anaphora
        feature_vector.append( same_sentence and anaphoric_pronoun)
        
        # grammar
        # ? not only bool for equality, but also categories ?
        feature_vector.append( self.has_feature( node, "Case", candidate.feats['Case'].split( ','))) # same case
        feature_vector.append( self.has_feature( node, "Gender", candidate.feats['Gender'].split( ','))) # same gender
        feature_vector.append( self.has_feature( node, "Number", candidate.feats['Number'].split( ','))) # same number
        feature_vector.append( self.has_feature( node, "Person", candidate.feats['Person'].split( ','))) # same person
        
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
        feature_vector.append( candidate.udeprel == "nsubj" or  candidate.udeprel == "csubj" ) # subject        
        
        # target_value
        if ( self.for_training() ):
            feature_vector.append( self.are_coreferents( node, candidate))
        
        feature_vector.append(node.form)        
        feature_vector.append(candidate.form)
        
        feature_vector.append(node_bundle.bundle_id)
        feature_vector.append(node.ord)
        
        feature_vector.append(candidate_bundle.bundle_id)
        feature_vector.append(candidate.ord)
        
        self.feature_vectors.append( feature_vector)
    
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
    
    def has_deprel( self, node, list_of_possible_deprels): # -> bool
        """
        controls if the node's deprel is on of the possible ones
        """     
        return ( node.deprel in list_of_possible_deprels )
        
    def get_bundle( self, root_path):
        root = root_path[0]
        return root.bundle
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
    
    def get_depth( self, root_path):
        return len( root_path) - 1
    def get_ccs_depth( self, root_path_1, root_path_2): # closest common supernode
        it = 0
        while ( it < len( root_path_1) and it < len( root_path_2) and root_path_1[it] == root_path_2[it] ):
            it += 1
        return it - 1        
    
    def get_root_path(self, node):
        root_path = [ node ]
        n = node        
        while ( not n.is_root() ):            
            n = n.parent
            root_path = [ n ] + root_path
        return root_path    
    
