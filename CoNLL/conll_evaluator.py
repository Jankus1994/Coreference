# Jan Faryad
# 4. 5. 2017
#
# evaluation of automatic recognition of coreference

from conll_processor import CoNLL_processor
from conll_api import CoNLL_API as api

class CoNLL_evaluator:
    def __init__( self, gold_input, auto_input):
        self.gold_doc = CoNLL_processor( gold_input).process_document()
        self.auto_doc = CoNLL_processor( auto_input).process_document()
    def evaluate( self):
        """
        main method for evaluation
        """
        gold_coreferents = self.get_corefs( self.gold_doc) # what was supposed to be decided
        auto_coreferents = self.get_corefs( self.auto_doc) # what was decided
        
        gold_coref_ids = [ coref.coref_id for coref in gold_coreferents ] # ids
        auto_coref_ids = [ coref.coref_id for coref in auto_coreferents ]
        
        # words that that were supposed to be decided and also were. still clusters may differ
        common_gold_coreferents = [ coref for coref in gold_coreferents if ( coref.coref_id in auto_coref_ids ) ]
        common_auto_coreferents = [ coref for coref in auto_coreferents if ( coref.coref_id in gold_coref_ids ) ]
        if ( len( common_gold_coreferents) == len( common_auto_coreferents) ): # should hold
            relevants = len( gold_coreferents)
            selecteds = len( auto_coreferents)
            true_positives = 0 # number of correctly decided
            for i in range( len( common_gold_coreferents)):
                gold_coref = common_gold_coreferents[i] # lists have the same ordering, so these two records refer to the same word
                auto_coref = common_auto_coreferents[i]
                gold_cluster = gold_coref.cluster # cluster assigned to this word in gold and auto data
                auto_cluster = auto_coref.cluster
                if ( self.compare_clusters( gold_cluster, auto_cluster) ): # comparing, if the the clusters have at least one other common word
                    true_positives += 1
            precision = true_positives / float( selecteds) # output values describing the quality of automatical recognition
            recall = true_positives / float( relevants)
            """
            print( "Selected pronouns:\t\t\t", selecteds)
            print( "Relevant pronouns:\t\t\t", relevants)
            print( "Selected relevant:\t\t\t", len( common_gold_coreferents))
            print( "Correctly decided:\t\t\t", true_positives)
            print( "")
            print( "Precision:\t\t\t", precision)
            print( "Recall:\t\t\t", recall)
            """
            return ( precision, recall )
            
        
    def compare_clusters( self, cluster_1, cluster_2): # -> bool
        """
        if two given clusters have at least two common word ids
        one of the word, which is beaing checked, if its coreference was decided correctly
        this word has one cluster in the gold data, other in auto. now we are checking, if the clusters are identical:
        is there another common word in both clusters?
        """
        common = set( cluster_1.coref_ids) & set( cluster_2.coref_ids)
        return ( len( common) > 1 )
        
    def get_corefs( self, doc): # -> list of coreferenting expression (represented by Eval_coref_record object) in the given Document
        clusters = [] # list of Eval_cluster_records
        coreferents = [] # list of Eval_coref_records
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
        return coreferents

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
        
