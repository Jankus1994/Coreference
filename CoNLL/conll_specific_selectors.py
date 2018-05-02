# Jan Faryad
# 10. 3. 2018
#
# feature selectors for individual pronoun types
# they define the list of possible upostag for pronouns and their coreferencre candidates and add som specific features to the general ones (see selector)
from udapi.block.demo.Coreference.CoNLL.conll_selector import Conll_selector

class Conll_rel_selector( Conll_selector):
    def __init__( self):
        self.pron_type = "Rel"
        self.possible_pronoun_upostags = [ "PRON", "DET" ]
        self.possible_candidate_upostags = [ "NOUN", "PRON", "DET", "VERB", "PROPN", "NUM" ]
    def node_filter( self, node):
        return ( node.upos in self.possible_pronoun_upostags and self.pron_type in node.feats[ "PronType" ] )
    
    def specific_features( self, node, candidate, feature_vector): # void
        
        basic_relpron_relation = False
        parent = node.parent
        if ( parent != None ):
            grandparent = parent.parent
            if ( grandparent != None ):
                if ( grandparent == candidate ):
                    basic_relpron_relation = True
        feature_vector.append( basic_relpron_relation) # relative pronoun is dependet on the verb - head of the subclause, which is dependet on the referent of the pronoun

class Conll_dem_selector( Conll_selector):
    def __init__( self):
        self.pron_type = "Dem"    
        self.possible_pronoun_upostags = [ "PRON", "DET" ]        
        self.possible_candidate_upostags = [ "NOUN", "PRON", "DET", "VERB"]#, "PROPN" ] #, "AUX", "CCONJ" ]
    def node_filter( self, node):
        return ( node.upos in self.possible_pronoun_upostags and self.pron_type in node.feats[ "PronType" ] )
    
    def specific_features( self, node, candidate, feature_vector): # void
        same_bundle = ( node.root.bundle.bundle_id == candidate.root.bundle.bundle_id )
        previous_bundle = ( int( node.root.bundle.bundle_id) == int( candidate.root.bundle.bundle_id) + 1 ) 

        # root of the previous sentence - the pronoun referes to all what was said there
        root_candidate = ( candidate.udeprel == "root" )
        feature_vector.append( root_candidate and previous_bundle )
        
        # xcomp of the previous or the actual sentence
        xcomp_candidate = ( candidate.udeprel == "xcomp" )   
        feature_vector.append( xcomp_candidate)# and ( same_bundle or previous_bundle ) ) 
        
        obj_candidate = ( "obj" in candidate.udeprel )   
        feature_vector.append( obj_candidate)

class Conll_prs_selector( Conll_selector):
    def __init__( self):
        self.pron_type = "Prs"    
        self.possible_pronoun_upostags = [ "PRON", "DET" ]
        self.possible_candidate_upostags = [ "NOUN", "PRON", "DET", "VERB", "PROPN" ]
    def node_filter( self, node):
        return ( node.upos in self.possible_pronoun_upostags and self.pron_type in node.feats[ "PronType" ] )
    
    def specific_features( self, node, candidate, feature_vector): # void
        
        same_bundle = ( node.root.bundle.bundle_id == candidate.root.bundle.bundle_id )
        previous_bundle = ( int( node.root.bundle.bundle_id) == int( candidate.root.bundle.bundle_id) + 1 )         
        #previous_bundle_2 = ( int( node.root.bundle.bundle_id) == int( candidate.root.bundle.bundle_id) + 2 )
        #previous_bundle_3 = ( int( node.root.bundle.bundle_id) == int( candidate.root.bundle.bundle_id) + 3 )
        
        # nsubj of the actual sentence + reflexive pronoun
        root_candidate = ( candidate.udeprel == "nsubj" )
        reflexive_node = ( "Yes" in node.feats[ "Reflex" ] )
        node_nonexpl = ( "expl" not in node.udeprel )
        feature_vector.append( root_candidate and  same_bundle and reflexive_node and node_nonexpl )
        
        noun_candidate = ( candidate.upos == "NOUN" or  candidate.upos == "PROPN" )           
        
        same_gender = self.feature_equality( candidate, node, "Gender")
        same_number = self.feature_equality( candidate, node, "Number")
        
        # appropriate noun in the previous sentences
        feature_vector.append( noun_candidate and same_gender and same_number and previous_bundle)
        #feature_vector.append( noun_candidate and same_gender and same_number and previous_bundle_2)
        #feature_vector.append( noun_candidate and same_gender and same_number and previous_bundle_3)
        # appropriate noun in the actual sentence
        feature_vector.append( noun_candidate and same_gender and same_number and same_bundle)     
        
        # persons
        feature_vector.append( node.feats[ "Person" ] == "0")
        feature_vector.append( node.feats[ "Person" ] == "1")
        feature_vector.append( node.feats[ "Person" ] == "2")
        feature_vector.append( node.feats[ "Person" ] == "3")
        feature_vector.append( candidate.feats[ "Person" ] == "0")
        feature_vector.append( candidate.feats[ "Person" ] == "1")
        feature_vector.append( candidate.feats[ "Person" ] == "2")
        feature_vector.append( candidate.feats[ "Person" ] == "3")
        
class Conll_prodrop_selector( Conll_selector):
    def __init__( self):
        self.possible_pronoun_upostags = [ "VERB" ]
        self.possible_candidate_upostags = [ "NOUN", "PRON", "DET", "PROPN" ]
    def node_filter( self, node):
        # node is a main verb with no subject present in the sentence
        if ( node.upos in self.possible_pronoun_upostags and node.deprel == "root" ):
            number_of_subjects = len( [ child for child in node.children if ( "subj" in child.deprel ) ])
            if ( number_of_subjects == 0 ):
                return True
        return False
    
    def specific_features( self, node, candidate, feature_vector): # void
        pass

# final selectors definine a method, which says if the target value should be printed (for training) or not (for prediction)

class Conll_rel_prediction_selector( Conll_rel_selector):
    def for_training( self):
        return False
class Conll_rel_training_selector( Conll_rel_selector):
    def for_training( self):
        return True

class Conll_dem_prediction_selector( Conll_dem_selector):
    def for_training( self):
        return False
class Conll_dem_training_selector( Conll_dem_selector):
    def for_training( self):
        return True

class Conll_prs_prediction_selector( Conll_prs_selector):
    def for_training( self):
        return False
class Conll_prs_training_selector( Conll_prs_selector):
    def for_training( self):
        return True

class Conll_prodrop_prediction_selector( Conll_prodrop_selector):
    def for_training( self):
        return False
class Conll_prodrop_training_selector( Conll_prodrop_selector):
    def for_training( self):
        return True
