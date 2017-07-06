# Jan Faryad
# 3. 7. 2017
#
# extracting information about coreference from onf file

class Onto_coreference_getter:
    def __init__( self, onto_input):
        """ onto input ... onf file """
        self.onto_input = onto_input        
    
    def process_file( self):
        """
        main method, calle from outside
        reads the "Coreference chains" parts in the onf file, where
        the coreference clusters for each section are enumerated
        """
        list_of_clusters = []
        
        active_chains = False # if we are in the the "Coreference chains" block which comes after each section (text, set of sentences)
        active_cluster = False # if we are in one particular cluster
        for line in self.onto_input:
            if ( "Coreference chains" in line ): # beginning of the enumeration of clusters
                active_chains = True
            elif ( "Plain sentence" in line ): # new sentence -> end of the enumeration
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
                    ( position_string, expression ) = processed # coreferenting expression (not only head, but the whole "subtree"
                                                                # position string: a.b-c, a = sentence number, b/c = first/last word number
                    coreferent = Onto_coreferent( position_string, expression)
                    cluster.add_coref( coreferent)
        
        return list_of_clusters
                
    def process_coref_line( self, line): # -> ( string, string )
        """ getting of the coreferenting expression and its position """
        line_list = line.split( ' ')
        if ( len( line_list) < 17 ):
            return None
        position = line_list[15] # position string begins at this position and doesn't have spaces
        if ( position == "" ):
            return None
        if ( len( line) < 26 ):
            return None
        expression = line[26:-1] # expression begins at this position and does have spaces
        return ( position, expression )

class Onto_coreferent:
    def __init__( self, position_string, form):
        self.position_string = position_string # string
        self.form = form # string, the coreferenting word
class Onto_cluster:
    def __init__( self):
        self.coreferents = [] # Onto_coreferents, but later (after conversion) Nodes
    def add_coref( self, coref):
        self.coreferents.append( coref)
                
