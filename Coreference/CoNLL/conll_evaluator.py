# Jan Faryad
# 4. 5. 2017
#
# evaluation of automatic recognition of coreference

from conll_processor import CoNLL_processor
from conll_api import CoNLL_API as api
import sys

class CoNLL_evaluator:
    def __init__( self, gold_input_name, auto_input_name):
        self.gold_input = open( gold_input_name, 'r')
        self.auto_input = open( auto_input_name, 'r')
    def evaluate( self):
        """
        main method for evaluation
        """
        precision_sum = 0
        recall_sum = 0
        
        # lists of Eval_coref_records
        gold_coreferents = self.get_corefs( self.gold_input) # what was supposed to be decided
        auto_coreferents = self.get_corefs( self.auto_input) # what was decided
        
        print(len( gold_coreferents), len( auto_coreferents))
        
        if ( len( gold_coreferents) == 0 ):
            return( 1, 1)
        if ( len( auto_coreferents) == 0 ):
            return( 0, 0)
        
        gold_coref_ids = [ coref.coref_id for coref in gold_coreferents ] # ids
        auto_coref_ids = [ coref.coref_id for coref in auto_coreferents ]
        #union_coref_ids = list( set( gold_coref_ids) | set( auto_coref_ids))                     
        
        # words that that were supposed to be decided and also were. still clusters may differ
        common_gold_coreferents = [ coref for coref in gold_coreferents if ( coref.coref_id in auto_coref_ids ) ]
        common_auto_coreferents = [ coref for coref in auto_coreferents if ( coref.coref_id in gold_coref_ids ) ]
        if ( len( common_gold_coreferents) == len( common_auto_coreferents) ): # should hold
            common_corefs_number = len( common_gold_coreferents)
            for i in range( common_corefs_number):
                gold_coref = common_gold_coreferents[i] # lists have the same ordering, so these two records refer to the same word
                auto_coref = common_auto_coreferents[i]
                gold_cluster = gold_coref.cluster # cluster assigned to this word in gold and auto data
                auto_cluster = auto_coref.cluster
                
                if (len( gold_cluster.coref_ids) == 1): # drops
                    continue
                
                # "-1" in the next: not counting the actual coreferent
                gold_size = len( gold_cluster.coref_ids) - 1 # relevant coreferents to this word 
                auto_size = len( auto_cluster.coref_ids) - 1 # selected coreferents to this word
                inter_size = len( set( gold_cluster.coref_ids) & set( auto_cluster.coref_ids)) - 1
                prec = inter_size / float( auto_size)
                rec = inter_size / float( gold_size)
                precision_sum += prec
                recall_sum += rec
                #print(prec, rec)
                #if ( auto_size != inter_size or gold_size != inter_size):
                    #print( auto_size, gold_size, inter_size)
            #"""
            #print( "Selected pronouns:\t\t\t", len( auto_coreferents))
            #print( "Relevant pronouns:\t\t\t", len( gold_coreferents))
            #print( "Selected relevant:\t\t\t", len( common_gold_coreferents))
            #print( "Correctly decided:\t\t\t", true_positives)
            #print( "")
            print( "Precision:  " + str( precision_sum / len( auto_coreferents))) # teraz je vysledok ohrsi kvoli vyskrtnuti koreferentov prodropov
            print( "Recall:     " + str( recall_sum / len( gold_coreferents)))
            #"""
            # if an id is missing in one of the id-lists, it will contribute 0 to precision/recall sum, but 1 to the divisor
            return ( precision_sum / len( auto_coreferents), recall_sum / len( gold_coreferents) )
            
        
    def compare_clusters( self, cluster_1, cluster_2): # -> bool
        """
        if two given clusters have at least two common word ids
        one of the word, which is beaing checked, if its coreference was decided correctly
        this word has one cluster in the gold data, other in auto. now we are checking, if the clusters are identical:
        is there another common word in both clusters?
        """
        common = set( cluster_1.coref_ids) & set( cluster_2.coref_ids)
        return ( len( common) > 1 )
        
    def get_corefs( self, input_file): # -> list of coreferenting expression (represented by Eval_coref_record object) in the given conll file        
        clusters = [] # list of Eval_cluster_records
        coreferents = [] # list of Eval_coref_records
        sent_id = 0
        for line in input_file:
            if ( line == '\n' ): # blank line
                sent_id += 1
            elif ( line != '\n' and line[0] != '#' ): # not comment line -> record line
                fields = line[:-1].split( '\t')
                if ( len( fields) == 10 ): 
                    misc = fields[-1]
                    misc_fields = misc.split( '|')
                    coref = [ misc_field for misc_field in misc_fields if "Coref" in misc_field ]
                    if ( len( coref) > 0 ):
                        cluster_id = int( coref[0].split( '=')[1])
                        # there should be at most one such cluster
                        appropriate_clusters = [ cluster for cluster in clusters if ( cluster.cluster_id == cluster_id ) ]
                        if ( appropriate_clusters == [] ): # first occurence of this cluster id - create a new instance
                            cluster = Eval_cluster_record( cluster_id)
                            clusters.append( cluster)
                        else: # already existing cluster
                            cluster = appropriate_clusters[0] # there is at most one element
                        word_id = int( fields[0])
                        coref_id = ( sent_id, word_id )
                        cluster.add_coreferent( coref_id) # adding coreferent id to the list of coreferents of the cluster
                        #if ( api.has_upostag( node, [ "PRON", "DET" ]) # if we are supposed to detect coreference of this cluster
                        #     and api.has_feature( node, "PronType", [ "Prs", "Rel", "Dem" ]) ):
                        #    # !!! PRO DROPS MISSING !!!
                        coref = Eval_coref_record( coref_id, cluster)
                        coreferents.append( coref) # output list of all pronouns, for which the coreference was detected                        
                        
                        
        """            
        for paragraph in api.get_paragraphs( doc):         # linear iteration through all nodes in the document
            for sentence in api.get_sentences( paragraph): #
                for node in api.get_nodes( sentence):      #
                    cluster_id_string = api.get_misc_by_name( node, "Coref") # getting coreference cluster number (string)
                    if ( cluster_id_string == None ):
                        cluster_id_string = api.get_misc_by_name( node, "Drop_coref") # !!! DROPS ARE IGNORED FOR NOW, IF THERE IS A NON-DROPPED COREFEREN !!
                    if ( cluster_id_string != None ):
                        cluster_id = int( cluster_id_string)
                        # there should be at most one such cluster
                        appropriate_clusters = [ cluster for cluster in clusters if ( cluster.cluster_id == cluster_id ) ]
                        if ( appropriate_clusters == [] ): # first occurence of this cluster id - create a new instance
                            cluster = Eval_cluster_record( cluster_id)
                            clusters.append( cluster)
                        else: # already existing cluster
                            cluster = appropriate_clusters[0] # there is at most one element
                        coref_id = api.get_full_id( node)                        
                        cluster.add_coreferent( coref_id) # adding coreferent to list of coreferents of the cluster
                        if ( api.has_upostag( node, [ "PRON", "DET" ]) # if we are supposed to detect coreference of this cluster
                             and api.has_feature( node, "PronType", [ "Prs", "Rel", "Dem" ]) ):
                            # !!! PRO DROPS MISSING !!!
                            coref = Eval_coref_record( coref_id, cluster)
                            coreferents.append( coref) # output list of all pronouns, for which the coreference was detected
        """
        
        return coreferents
    
    def get_coref_record_by_id( self, coreferents, id):
        for coref in coreferents:
            if ( coref.coref_id == id ):
                return coref

class Eval_cluster_record:
    def __init__( self, cluster_id):
        self.cluster_id = cluster_id
        self.coref_ids = []
    def add_coreferent( self, coref_id):
        self.coref_ids.append( coref_id)
class Eval_coref_record:
    def __init__( self, coref_id, cluster):        
        self.coref_id = coref_id
        self.cluster = cluster
        
if ( len( sys.argv) == 3 ):
    e = CoNLL_evaluator(sys.argv[1], sys.argv[2])
    e.evaluate()

        
