# Jan Faryad
# 20. 4. 2017
#
# static class for serving as interface for operations over processed document

from math import fabs

class CoNLL_API:
    """
    static class for serving as interface for operations over processed document
    """
    # NODE API
    # fields getters    
    def get_id( node): # -> int ( -1 for range nodes )
        return node.id
    def get_form( node): # -> string
        return node.form
    def get_lemma( node): # -> string
        return node.lemma
    def get_upostag( node): # -> string
        return node.upostag
    def get_xpostag( node): # -> string, NOT USED (language specific)
        return node.xpostag
    def get_feats( node): # -> list of features, feature = pair (name=string, list of values), value = string
        return node.feats
    def get_head( node): # -> Node
        return node.head
    def get_deprel( node): # -> string
        return node.deprel
    def get_deps( node): # -> list of secondary dependencies, = pair ( head=Node, name=string)
        return node.deps
    def get_misc( node): # -> list of other information, = pair (name=string, value=string)
        return node.misc
    
    def get_full_id( node): # -> triplet of ints
        """
        unique node id in the whole document
        """
        para_id = node.sentence.paragraph.number
        sent_id = node.sentence.number
        return ( para_id, sent_id, node.id )
    
    def has_upostag( node, list_of_possible_upostags): # -> bool
        """
        controls if the node's upostag is on of the possible ones
        """
        return ( node.upostag in list_of_possible_upostags )
    def has_feature( node, feature_name, list_of_possible_values): # -> bool
        """
        controls if the node has the given feature and if one of it's values is possible
        """
        for feat in node.feats:
            if ( feat[0] == feature_name ):
                # if the intersection of the present and possible values is non-empty
                return ( len( set( feat[1]) & set( list_of_possible_values) ) > 0 )                
                # for value in feat[1]:
                #     if ( value in list_of_possible_values ):
                #         return True
        return False
    def has_deprel( node, list_of_possible_deprels): # -> bool
        """
        controls if the node's dependecy relation is on of the possible ones
        """        
        return ( node.deprel in list_of_possible_deprels )   
    def get_features_by_name( node, name): # -> list of strings
        """
        returns the list of values of the given feature (empty if the feature is ont present)
        """
        for feat in node.feats:
            if ( feat[0] == name ):
                return feat[1]
        return []
    def get_misc_by_name( node, name): # -> string
        """
        returns value of the given misc
        """
        for misc in node.misc:
            if ( misc[0] == name ):
                return misc[1]
        return None    
    
    
    def is_leaf( node): # -> bool
        return ( node.subnodes == [] )
    def is_range_node( node): # -> bool
        return ( node.depth == -1 )
    def get_depth( node): # -> int ( -1 for range nodes )
        return node.depth
    def get_subnodes_number( node): # -> int
        return len( node.subnodes)
    def get_subnodes( node): # -> list of Nodes
        return node.subnodes
    def get_root_path( node): # -> list of Nodes
        return node.root_path
    def get_sentence( node): # -> Sentence
        return node.sentence 
    
    # SENTENCE, PARAGRAPH AND DOCUMENT API
    def get_root( sent): # -> Node
        return sent.root
    def get_depth( sent): # -> int
        return sent.depth
    def get_nodes_number( sent): # -> int
        return sent.nodes_number
    def get_nodes( sent): # -> list of Nodes
        return sent.nodes
    
    def get_sentences( para): # -> list of Sentences
        return para.sentences  
    def get_paragraphs( doc): # -> list of Paragraphs
        return doc.paragraphs    
    
    def previous_paragraph( para): # -> Paragraph, None for the first paragraph in the document
        index_of_previous = para.number - 2 # list indeces from 0
        if ( index_of_previous >= 0 ):
            return para.document.paragraphs[ index_of_previous ]
    def next_paragraph( para): # -> Paragraph, None for the last paragraph in the document
        index_of_next = para.number # list indeces from 0
        if ( index_of_next < len( para.document.paragraphs) ):
            return para.document.paragraphs[ index_of_next ]
    def previous_sentence( sent): # -> Sentence, None for the first sentence in the paragraph
        index_of_previous = sent.number - 2 # list indeces from 0
        if ( index_of_previous >= 0 ):
            return sent.paragraph.sentences[ index_of_previous ]
        else:
            prev_para = CoNLL_API.previous_paragraph( sent.paragraph) # possibly in the previous paragraph
            if ( prev_para != None ):
                return prev_para.sentences[-1]
    def next_sentence( sent): # -> Sentence, None for the last sentence in the paragraph
        index_of_next = sent.number # list indeces from 0
        if ( index_of_next < len( sent.paragraph.sentences) ):
            return sent.paragraph.sentences[ index_of_next ]     
        else:
            next_para = CoNLL_API.next_paragraph( sent.paragraph) # possibly in the next paragraph
            if ( next_para != None ):
                return next_para.sentences[0]
    
    # TWO NODES RELATION
    def in_same_sentence( node_1, node_2): # -> bool
        return ( node_1.sentence == node_2.sentence )
    def in_same_paragraph( node_1, node_2): # -> bool
        return ( node_1.sentence.paragraph == node_2.sentence.paragraph )
    def surface_node_distance( node_1, node_2): # -> int
        """
        surface distance of two words in the sentence, -1 if they are not the the same sentence
        """
        if ( not CoNLL_API.in_same_sentence( node_1, node_2) ):
            return -1
        values = [ fabs( node_1.id_range[0] - node_1.id_range[1] ), # general, works also for range nodes
                   fabs( node_1.id_range[1] - node_1.id_range[0] ) # don't know, which one come first
                 ]
        return int( round( min( values)))
    def surface_sentence_distance( node_1, node_2): # -> int
        """
        surface distance of the sentences of two words in the paragraph, -1 if they are not the the same paragraph
        """        
        if ( not CoNLL_API.in_same_paragraph( node_1, node_2) ):
            return -1
        return int( round( fabs( node_1.sentence.number - node_2.sentence.number)))
    def surface_paragraph_distance( node_1, node_2): # -> int
        """
        surface distance of the paragraphs of two words in the documet
        """            
        return int( round( fabs( node_1.sentence.paragraph.number - node_2.sentence.paragraph.number)))
    def depth_distance( node_1, node_2): # -> int
        """
        difference of depths
        """
        return int( round( fabs( CoNLL_API.get_depth( node_1) - CoNLL_API.get_depth( node_2))))
    def is_supernode_of( node_1, node_2): # -> bool
        return ( node_1 in node_2.root_path)
    def closest_common_supernode( node_1, node_2): # -> Node
        """
        first common supernode (coming upwards from the given nodes)
        """
        if ( not CoNLL_API.in_same_sentence( node_1, node_2) or CoNLL_API.is_range_node( node_1) or CoNLL_API.is_range_node( node_2) ):
            return None # not in the same sentence or one of the nodes is a range node
        ccs = node_1.sentence.root # == node_2.sentence.root
        ran = min( len( node_1.root_path), len( node_2.root_path)) # meaningful only to the lower depth of the nodes
        for i in range( ran):
            if ( node_1.root_path[i] == node_2.root_path[i] ):
                ccs = node_1.root_path[i]
            else:
                return ccs
        return ccs # == one of the given nodes
    def ccs_depth( node_1, node_2): # -> int
        """
        depth of the closest common supernode, -1 if they don't have a ccs
        """
        ccs = CoNLL_API.closest_common_supernode( node_1, node_2)
        if ( ccs == None ):
            return -1
        return CoNLL_API.get_depth( ccs)
    def compound_distance( node_1, node_2): # -> int
        """
        sum of sistances from ccs, -1 if no ccs exist
        """
        ccs = CoNLL_API.closest_common_supernode( node_1, node_2)
        if ( ccs == None ):
            return -1
        return CoNLL_API.depth_distance( node_1, ccs) + CoNLL_API.depth_distance( node_2, ccs)
    
    # TARGET
    def are_coreferents( node, candidate): # -> bool
        """
        if two nodes are in the same coreference cluster
        """
        coref_1 = CoNLL_API.get_misc_by_name( node, "Coref")
        drop_coref_1 = CoNLL_API.get_misc_by_name( node, "Drop_coref")
        coref_2 = CoNLL_API.get_misc_by_name( candidate, "Coref")
        drop_coref_2 = CoNLL_API.get_misc_by_name( candidate, "Drop_coref")
        for c in [ coref_1, drop_coref_1 ]:
            if ( c != None and c in [ coref_2, drop_coref_2 ] ):
                return True
        return False

        
            
            
            
            
            
            
            
            
            
            
            
            
            
