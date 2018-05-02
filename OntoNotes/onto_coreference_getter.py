# Jan Faryad
# 3. 7. 2017
#
# second part of coreference transcription from ontonotes: extracting information about coreference from onf files

from udapi.block.demo.Coreference.OntoNotes.onto_cluster import Onto_cluster
from udapi.block.demo.Coreference.OntoNotes.onto_coreferent import Onto_coreferent

class Onto_coreference_getter:    
    def execute( self, filename): # -> list of onto clusters
        """
        main method, called from outside
        reads the "Coreference chains" parts in the onf file, where
        the coreference clusters for each section are enumerated
        """
        onto_input = open( filename + ".onf", 'r')  
        
        list_of_clusters = []
        
        active_chains = False # if we are in the "Coreference chains" block which comes after each section (text, set of sentences)
        active_cluster = False # if we are in one particular cluster within this block
        for line in onto_input:
            if ( "Coreference chains" in line ): # beginning of the enumeration of clusters
                active_chains = True
            elif ( "Plain sentence" in line ): # new sentence -> new section -> end of the enumeration
                active_chains = False            
            elif ( active_chains and "(IDENT)" in line ): # new cluster
                active_cluster = True
                cluster = Onto_cluster()
                list_of_clusters.append( cluster)
            elif ( active_chains and line == '\n' ): # end of the cluster
                active_cluster = False
            
            elif ( active_cluster ): # coreferent in the cluster
                processed = self.process_coref_line( line)
                if ( processed != None ):
                    ( position_string, expression ) = processed # corefering expression (not only head, but the whole "subtree"
                                                                # position string: a.b-c, a = sentence number, b/c = first/last word number
                    onto_coreferent = Onto_coreferent( position_string, expression)
                    cluster.add_onto_coreferent( onto_coreferent)
        
        onto_input.close()
        return list_of_clusters
                
    def process_coref_line( self, line): # -> ( string, string )
        """ getting of the coreferenting expression and its position """
        NUMBER_OF_SPACES = 16 # before the coreference string begins
        EXPRESSION_POSITION = 26 # the expression begins at this position
        line_list = line.split( ' ')
        if ( len( line_list) < NUMBER_OF_SPACES + 1 ): # there should be at least one character except the spaces
            return None
        position = line_list[ NUMBER_OF_SPACES - 1] # position string begins at this position and doesn't have spaces
        if ( position == "" ):
            return None
        if ( len( line) < EXPRESSION_POSITION ):
            return None
        expression = line[ EXPRESSION_POSITION : -1 ]
        return ( position, expression )
