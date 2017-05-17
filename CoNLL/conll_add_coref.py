# Jan Faryad
# 30. 4. 2017
#
# adding detected coreference to the plain (without coreference) conll-u file  (outp)

from auxiliaries import join_with_separator

class CoNLL_add_coreference:
    def __init__( self, input, output):
        self.input = input
        self.output = output
        self.list_of_coreferents = []
    
    def add_coreference( self, list_of_triplets): # void
        """
        list of triplets ( pronoun id, candidate id, bool ~ are coreferents )
        main method for adding detected coreference information
        """
        self.build_clusters( list_of_triplets)
        
        iterator = 0
        para_id = 0                  
        sent_id = 0 
        for line in self.input:
            if ( len( self.list_of_coreferents) > iterator ):
                actual_coreferent = self.list_of_coreferents[ iterator ]
            else:
                actual_coreferent = None
            
            fields = line.split( '\t')
            if ( line[0] == '#' ): # comment line beginning with #                
                if ( len( fields) == 4 and fields[1] == '$' ): # new sentence with paragraph and sentence id
                    para_id = int( fields[2])                    
                    sent_id = int( fields[3])
                self.output.write( line)
            elif ( line != ' \n' ): # not a blank line -> record line
                try:
                    word_id = int( fields[0])
                    if ( actual_coreferent != None and actual_coreferent.id == ( para_id, sent_id, word_id ) ):
                        misc = fields[-1] # adding to the last column
                        coref_info = "Coref=" + str( actual_coreferent.cluster_id)
                        if ( misc == "_\n" or misc == "_" ): # no other information in the column
                            new_misc = coref_info + "\n"
                        else: # adding to another information
                            new_misc = misc[:-1] + "|" + coref_info + "\n" # [:-1] ... except newline
                        new_line = join_with_separator( fields[:-1] + [ new_misc ], '\t') # rebuildng the line with the new last column
                        self.output.write( new_line)
                        iterator += 1
                        #actual_coreferent = self.list_of_coreferents[ iterator ]
                        continue                    
                    self.output.write( line)
                except: # range line
                    self.output.write( line)
            else: # blank line
                self.output.write( line)

    def build_clusters( self, list_of_triplets): # triplets( pronoun id, referent id, bool - are coreferents?)
        for triplet in list_of_triplets:
            if ( triplet[2] ): # if they are coreferents
                # obtaining Coreferents from ids
                pronoun = self.get_coreferent( triplet[0]) # these methos fill list of coreferents
                referent = self.get_coreferent( triplet[1])
                # connection between Coreferents
                pronoun.add_coreferent( referent)
                referent.add_coreferent( pronoun)
        
        # adding cluster id to all Coreferents in the cluster
        cluster_id = 0
        for coref in self.list_of_coreferents:
            if ( coref.cluster_id == -1 ): # if the cluster still doesn't have an id
                coref.rewrite_cluster_id( cluster_id) # recursion
                cluster_id += 1
                
    def get_coreferent( self, coreferent_id): # -> Coreferent
        """
        returns Coreferent by id - either existing or it newly created
        """
        for i in range( len( self.list_of_coreferents)):
            if ( coreferent_id < self.list_of_coreferents[i].id ): # new coreferent in the middle
                coreferent = Coreferent( coreferent_id)
                self.list_of_coreferents = self.list_of_coreferents[:i] + [ coreferent ] + self.list_of_coreferents[i:]
                return coreferent
            elif ( coreferent_id == self.list_of_coreferents[i].id ): # existing coreferent
                return self.list_of_coreferents[i]
        coreferent = Coreferent( coreferent_id) # new coreferent at the end
        self.list_of_coreferents.append( coreferent)
        return coreferent            
        
class Coreferent:
    def __init__( self, id): # id ... triplet ( para id, sent id, word id )
        self.id = id
        self.coreferents = []
        self.cluster_id = -1
    def add_coreferent( self, coreferent): # void
        if ( coreferent not in self.coreferents ):
            self.coreferents.append( coreferent)
    def rewrite_cluster_id( self, new_cluster_id): # void
        """
        recursive method for setting cluster id to all coreferents in the cluster
        """
        if ( self.cluster_id != new_cluster_id ):
            self.cluster_id = new_cluster_id
            for coref in self.coreferents:
                coref.rewrite_cluster_id( self.cluster_id)