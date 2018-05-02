# Jan Faryad
# 10. 3. 2018
#
# selection of features for feature vectors

import math

class Conll_selector():
    def __init__( self):
        # to be overloaded
        self.pron_type = None
    def process_node( self, node, doc):
        self.doc = doc
        self.feature_vectors = []
        if ( self.node_filter( node) ): # see specific selectors
            self.search_candidate_nodes( node)
        return self.feature_vectors
    
    def search_candidate_nodes( self, pronoun_node): # void
        """ selects possible coreferents of the given pronoun_node """        
        actual_bundle = pronoun_node.root.bundle
        self.search_bundle_for_candidate_nodes( pronoun_node, actual_bundle)
        
        backwards_distance = 1 # 3 previous sentences
        previous_bundle = self.previous_bundle( actual_bundle)                
        for i in range( backwards_distance):
            if ( previous_bundle != None ):
                self.search_bundle_for_candidate_nodes( pronoun_node, previous_bundle)
                previous_bundle = self.previous_bundle( previous_bundle)
        
        #next_bundle = self.next_bundle( actual_bundle)
        #if ( next_bundle != None ):
            #self.search_bundle_for_candidate_nodes( pronoun_node, next_bundle)
        
    def search_bundle_for_candidate_nodes( self, pronoun_node, bundle): # void
        """ candidate_nodes from the given setences """
        root = bundle.trees[0]
        for candidate_node in root.descendants:
            if ( self.consider_candidate_node( pronoun_node, candidate_node) ):
                self.build_feature_vector( pronoun_node, candidate_node)

    def consider_candidate_node( self, pronoun_node, candidate_node): # -> bool
        """ if "candidate_node" is an appropriate candidate_node for coreference with "pronoun_node" """
        if ( pronoun_node == candidate_node ):
            return False
        # if "candidate_node" has an aprropriate POS - it differs according to pronoun type of "pronoun_node"
        # specifc selectors have different list of possible upostags
        if ( candidate_node.upos in self.possible_candidate_upostags ):            
            return True          
        return False
    
    def build_feature_vector( self, pronoun_node, candidate_node): # void
        """selecting and printing features for the given pair pronoun_node-candidate_node """
        feature_vector = []
        pronoun_node_root_path = self.get_root_path( pronoun_node)
        candidate_node_root_path = self.get_root_path( candidate_node)
        pronoun_node_bundle = pronoun_node.root.bundle
        candidate_node_bundle = candidate_node.root.bundle
        same_sentence = ( pronoun_node_bundle == candidate_node_bundle )
        
        #
        # distances
        feature_vector.append( same_sentence)
        
        if ( same_sentence ):
            feature_vector.append( int( math.fabs( pronoun_node.ord - candidate_node.ord)))
        else:
            feature_vector.append( int( math.fabs( int( pronoun_node_bundle.bundle_id) - int( candidate_node_bundle.bundle_id))))
        
        pronoun_node_depth = self.get_depth( pronoun_node_root_path)
        candidate_node_depth = self.get_depth( candidate_node_root_path)
        feature_vector.append( pronoun_node_depth)
        feature_vector.append( candidate_node_depth)
        feature_vector.append( int( math.fabs( pronoun_node_depth - candidate_node_depth)))
        # common depth
        common_depth = self.get_common_depth( pronoun_node_root_path, candidate_node_root_path)
        feature_vector.append( common_depth)
        # compound distance - length of the path joining the pronoun_nodes
        feature_vector.append( int( math.fabs( pronoun_node_depth - common_depth)) + int( math.fabs( common_depth - candidate_node_depth)))
        
        anaphoric_pronoun = ( int( pronoun_node_bundle.bundle_id), pronoun_node.ord ) > ( int( candidate_node_bundle.bundle_id), candidate_node.ord ) # the pronoun is after its antecedent - anaphora
        feature_vector.append( same_sentence and anaphoric_pronoun)
        #
        # grammar
        feature_vector.append( self.feature_equality( candidate_node, pronoun_node, "Case")) # same case
        feature_vector.append( self.feature_equality( candidate_node, pronoun_node, "Gender")) # same gender
        feature_vector.append( self.feature_equality( candidate_node, pronoun_node, "Number")) # same number
        feature_vector.append( self.feature_equality( candidate_node, pronoun_node, "Person")) # same person

        # pronoun
        feature_vector.append( "Dem" in pronoun_node.feats[ "PronType" ]) # demonstrative
        feature_vector.append( "Prs" in pronoun_node.feats[ "PronType" ]) # personal
        feature_vector.append( "Rel" in pronoun_node.feats[ "PronType" ]) # relative
        feature_vector.append( "Yes" in pronoun_node.feats[ "Reflex" ]) # reflexive
        feature_vector.append( "Yes" in pronoun_node.feats[ "Poss" ]) # possessive        

        # candidate_node
        # part of speech
        feature_vector.append( candidate_node.upos == "NOUN" )
        feature_vector.append( candidate_node.upos == "PRON" )
        feature_vector.append( candidate_node.upos == "VERB" )
        feature_vector.append( candidate_node.upos == "DET" )
        feature_vector.append( candidate_node.upos == "PROPN" )
        feature_vector.append( candidate_node.upos == "AUX" )
        feature_vector.append( candidate_node.upos == "ADP" )
        feature_vector.append( candidate_node.upos == "CCONJ" )
        feature_vector.append( candidate_node.upos == "SCONJ" )
        feature_vector.append( candidate_node.upos == "ADV" )
        feature_vector.append( candidate_node.upos == "PUNCT" )
        # deprels - sometimes it can have a form of "___:poss" et., so checking a substrig is better than equality
        feature_vector.append( "nsubj" in candidate_node.udeprel )
        feature_vector.append( "obj" in candidate_node.udeprel )
        feature_vector.append( "iobj" in candidate_node.udeprel )
        feature_vector.append( "csubj" in candidate_node.udeprel )
        feature_vector.append( "ccomp" in candidate_node.udeprel )
        feature_vector.append( "xcomp" in candidate_node.udeprel )
        feature_vector.append( "nmod" in candidate_node.udeprel )
        feature_vector.append( "acl" in candidate_node.udeprel )
        feature_vector.append( "compound" in candidate_node.udeprel )
        feature_vector.append( "aux" in candidate_node.udeprel )
        feature_vector.append( "det" in candidate_node.udeprel )
        feature_vector.append( "root" in candidate_node.udeprel )        

        # numbers
        feature_vector.append( "Sing" in pronoun_node.feats[ "Number" ])
        feature_vector.append( "Plur" in pronoun_node.feats[ "Number" ])
        feature_vector.append( "Ptan" in pronoun_node.feats[ "Number" ])
        feature_vector.append( "Sing" in candidate_node.feats[ "Number" ])
        feature_vector.append( "Plur" in candidate_node.feats[ "Number" ])
        feature_vector.append( "Ptan" in candidate_node.feats[ "Number" ])
        
        # genders
        feature_vector.append( "Masc" in pronoun_node.feats[ "Gender" ])
        feature_vector.append( "Fem"  in pronoun_node.feats[ "Gender" ])
        feature_vector.append( "Neut" in pronoun_node.feats[ "Gender" ])
        feature_vector.append( "Com"  in pronoun_node.feats[ "Gender" ])
        feature_vector.append( "Masc" in candidate_node.feats[ "Gender" ])
        feature_vector.append( "Fem"  in candidate_node.feats[ "Gender" ])
        feature_vector.append( "Neut" in candidate_node.feats[ "Gender" ])
        feature_vector.append( "Com"  in candidate_node.feats[ "Gender" ])                
        
        # features for specific pronoun type - see specific selectors
        self.specific_features( pronoun_node, candidate_node, feature_vector) # void
        
        # target_value
        if ( self.for_training() ): # only if we are selecting features for training, not for prediction
            feature_vector.append( self.are_coreferents( pronoun_node, candidate_node))
        
        # word forms - only not used by machine learning model, only for human orientation in the data
        feature_vector.append(pronoun_node.form)        
        feature_vector.append(candidate_node.form)
        
        # IDs of both pronoun_nodes, used only with prediction - if the coreference is recognized, it is added to the pronoun_nodes with these IDs
        feature_vector.append(pronoun_node_bundle.bundle_id)
        feature_vector.append(pronoun_node.ord)        
        feature_vector.append(candidate_node_bundle.bundle_id)
        feature_vector.append(candidate_node.ord)
        
        self.feature_vectors.append( feature_vector)
    
    def node_filter( self, pronoun_node):        
        """ filter of pronoun pronoun_nodes and candidate_node pronoun_nodes - to be overloaded in specific selectors """
        pass    

    def specific_features( self, pronoun_node, candidate_node, feature_vector): # void
        """ add som pronoun-type-specific features, see specific selectors """
        pass
    
    def for_training( self):
        """ if the selecor is supposed for training -> the coerference information will be used, or for prediction -> it won't """
        pass
    
    ## ## ## complementary interface
    
    # neighbouring bundles
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
    
    # coreference chcecking
    def are_coreferents( self, pronoun_node, candidate_node): # -> bool
        """ if two pronoun_nodes are in the same coreference cluster """
        coref_1 = pronoun_node.misc['Coref']
        drop_coref_1 = pronoun_node.misc['Drop_coref']
        coref_2 = candidate_node.misc['Coref']
        drop_coref_2 = candidate_node.misc['Drop_coref']

        
        for c in [ coref_1, drop_coref_1 ]:
            if ( c != "" and c in [ coref_2, drop_coref_2 ] ):                
                return True
        return False        
    
    def get_root_path(self, node): # -> list of udapi nodes
        """ list of nodes on the path from the given node to the root, including both ending nodes """
        root_path = [ node ]
        n = node        
        while ( not n.is_root() ):            
            n = n.parent
            root_path = [ n ] + root_path
        return root_path           
    
    def get_depth( self, root_path):
        return len( root_path) - 1
    def get_common_depth( self, root_path_1, root_path_2):
        """ depth of the closest common ancestor = depth of the smallest subtree includnig both nodes """
        it = 0
        while ( it < len( root_path_1) and it < len( root_path_2) and root_path_1[it] == root_path_2[it] ):
            it += 1
        return it - 1 
    
    def feature_equality( self, node_1, node_2, feature):
        """ if the two nodes (could) have the same value in the given category  """
        feat_1 = self.get_feature( node_1, feature)
        feat_2 = self.get_feature( node_2, feature)
        # if the feature is not present, it can mean both that the node doesn't have it or that it has it, but with no specific value, so all the values are possible
        if ( feat_1 == "" or feat_2 == "" ):
            return True
        feat_list_1 = feat_1.split( ',')
        feat_list_2 = feat_2.split( ',')
        intersection = set( feat_list_1) & set( feat_list_2)
        return ( len( intersection) > 0 )
    
    def get_feature( self, node, feature):
        # if a pronoun is possessive, we take [psor] features, not the main ones
        if ( node.feats[ "Poss" ] == "Yes" ):
            if ( feature in [ "Gender", "Number" ]  ):
                return node.feats[ feature + "[psor]"]
        return node.feats[ feature ]    
    
