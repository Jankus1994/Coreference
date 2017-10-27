# Jan Faryad
# 4. 5. 2017
#
# evaluation of automatic recognition of coreference

from udapi.core.block import Block
import sys
from udapi.block.demo.Coreference.CoNLL.conll_fields import Fields
from enum import Enum

class Conll_evaluator:
    def evaluate_all( self, namefile_name):
        """ Evaluation of more filse, whose name are stored in namefile_name """
        namefile = open( namefile_name, 'r')
        gold_coref_sum = 0 # from these values the results are computed
        auto_coref_sum = 0
        precision_sum  = 0
        recall_sum     = 0
        for name in namefile:
            gold_file_name = "test/" + name[:-1] + ".out.conllu"  # files which are going to be compared
            auto_file_name = "test/" + name[:-1] + ".auto.conllu"
            try:
                gold_file = open( gold_file_name, 'r')
            except:
                print( "File " + gold_file_name + " was not found.") 
                break
            try:                
                auto_file = open( auto_file_name, 'r')
            except:
                print( "File " + auto_file_name + " was not found.")
                break
            
            ( number_of_gold_corefs, number_of_auto_corefs, precision, recall) = self.evaluate( gold_file, auto_file) # comparision of this pair
            gold_coref_sum += number_of_gold_corefs
            auto_coref_sum += number_of_auto_corefs
            precision_sum  += precision
            recall_sum     += recall

        
        # printing results
        
        print("")
        print( "Gold coreferents:   ", gold_coref_sum)
        print( "Auto coreferents:   ", auto_coref_sum)
        print("")
        
        if ( gold_coref_sum == 0 ):
            recall = None
        else:
            recall = recall_sum / gold_coref_sum
            
        if ( auto_coref_sum == 0 ):
            precision = None
        else:
            precision = precision_sum / auto_coref_sum
        
        print( "Precision:  ", precision)
        print( "Recall:     ", recall)      
                
        
    def evaluate( self, gold_input, auto_input):     
        """ evaluation of one pair of files - with gold coreference and with automatic recognized """
        # lists of Eval_coref_records
        gold_coreferents = self.get_corefs( gold_input) # what was supposed to be decided
        auto_coreferents = self.get_corefs( auto_input) # what was decided
        
        # filtering corefering nouns etc. we are intereste inly in pronouns and dropped pronouns (see Coref_type)
        relevant_gold_coreferents = [ coref for coref in gold_coreferents if ( coref.coref_type != Coref_type.Irrelevant ) ]
        relevant_auto_coreferents = [ coref for coref in auto_coreferents if ( coref.coref_type != Coref_type.Irrelevant ) ]
        
        gold_coref_ids   = [ coref.coref_id for coref in relevant_gold_coreferents ]
        auto_coref_ids   = [ coref.coref_id for coref in relevant_auto_coreferents ]       
        common_coref_ids = list( set( gold_coref_ids) | set( auto_coref_ids))
        
        number_of_relevant = 0
        number_of_selected = 0
        recall_sum    = 0
        precision_sum = 0

        for coref_id in common_coref_ids:
            gold_coref = None # objects Eval_coref_record with this coref_id
            auto_coref = None            
            
            gold_coref_list = [ coref for coref in relevant_gold_coreferents if coref.coref_id == coref_id ]
            if ( gold_coref_list ):
                number_of_relevant += 1
                gold_coref = gold_coref_list[0]
            
            auto_coref_list = [ coref for coref in relevant_auto_coreferents if coref.coref_id == coref_id ]
            if ( auto_coref_list ):
                number_of_selected += 1
                auto_coref = auto_coref_list[0]     
            
            # if both were found = are in some cluster in both files, we compare these clusters
            # otherwise we have incremented corresponding number (relevant/seletced) without any addition to precision/recall some; this will do the penalization
            if ( gold_coref and auto_coref ): 
                # if types of corefs differ, each cluster describes something else (proper cluster of the coref x cluster of dropped pronoun)
                prec = 0
                rec  = 0
                if ( gold_coref.coref_type == Coref_type.Pronoun and auto_coref.coref_type == Coref_type.Pronoun ):
                    gold_cluster = gold_coref.cluster # proper cluster assigned to this coref
                    auto_cluster = auto_coref.cluster
                    if ( gold_cluster and auto_cluster ):
                        ( prec, rec ) = self.compare_clusters( gold_cluster, auto_cluster)
                elif ( gold_coref.coref_type == Coref_type.Dropped and auto_coref.coref_type == Coref_type.Dropped ):
                    gold_drop_cluster = gold_coref.drop_cluster # cluster assigned to a potential dropped descendant
                    auto_drop_cluster = auto_coref.drop_cluster                   
                    if ( gold_drop_cluster and auto_drop_cluster ):
                        ( prec, rec ) = self.compare_clusters( gold_drop_cluster, auto_drop_cluster)
                precision_sum += prec
                recall_sum    += rec
        
        # if the results was computed for each file separately
        if ( number_of_relevant == 0 ):
            recall = None
        else:
            recall = recall_sum / number_of_relevant
            
        if ( number_of_selected == 0 ):
            precision = None
        else:
            precision = precision_sum / number_of_selected         
        
        #print( "Precision:  ", precision)
        #print( "Recall:     ", recall) 
        
        return ( number_of_relevant, number_of_selected, precision_sum, recall_sum )
    
    def compare_clusters( self, cluster_1, cluster_2): # -> ( float, float ) ~ ( prec, rec )
        """ counts precision and recall of """
        # "-1" in the next: not counting the actual coreferent
        size_1     = len( cluster_1.coref_ids) - 1
        size_2     = len( cluster_2.coref_ids) - 1
        inter_size = len( set( cluster_1.coref_ids) & set( cluster_2.coref_ids)) - 1
        prec = inter_size / float( size_1)
        rec  = inter_size / float( size_2)   
        return ( prec, rec )
        
    def get_corefs( self, input_file): # -> list of corefering expression (represented by Eval_coref_record object) in the given conll file        
        """ gets coreferents in a CoNLL file """
        clusters = [] # list of Eval_cluster_records
        coreferents = [] # list of Eval_coref_records
        
        sent_id = 1
        for line in input_file:
            if ( line == "\n" ): # new sentence
                sent_id += 1
            elif ( line[0] != '#' ): # only record lines, omitting comment lines
                fields = line[:-1].split( '\t')
                word_id = fields[ Fields.ID ]
                misc = fields[ Fields.MISC ]
                if ( "Coref" in misc or "Drop_coref" in misc ): # coreferent
                    coref_id = ( sent_id, word_id )
                    misc_split = misc.split( '|')
                    cluster      = None
                    drop_cluster = None
                    for misc_record in misc_split:
                        ( attribute, value ) = misc_record.split( '=')
                        if ( attribute == "Coref" ):
                            cluster_id = int( value)
                            appropriate_clusters = [ cluster for cluster in clusters if ( cluster.cluster_id == cluster_id ) ]
                            if ( appropriate_clusters == [] ): # first occurence of this cluster id - create a new instance
                                cluster = Eval_cluster_record( cluster_id)
                                clusters.append( cluster)
                            else: # already existing cluster
                                cluster = appropriate_clusters[0] # there is at most one element
                            cluster.add_coreferent( coref_id) # adding coreferent id to the list of coreferents of the cluster                                
                        elif ( attribute == "Drop_coref" ):
                            drop_cluster_id = int( value)                            
                            appropriate_clusters = [ cluster for cluster in clusters if ( cluster.cluster_id == drop_cluster_id ) ]
                            if ( appropriate_clusters == [] ): # first occurence of this cluster id - create a new instance
                                drop_cluster = Eval_cluster_record( drop_cluster_id)
                                clusters.append( drop_cluster)
                            else: # already existing cluster
                                drop_cluster = appropriate_clusters[0] # there is at most one element
                            drop_cluster.add_coreferent( coref_id) # adding coreferent id to the list of coreferents of the cluster
                    coref_type = self.get_coref_type( fields[ Fields.UPOSTAG ], fields[ Fields.FEATS ]) # if we are supposed to detect coreference of this word
                    coref = Eval_coref_record( coref_id, cluster, drop_cluster, coref_type)
                    coreferents.append( coref) # output list of all pronouns, for which the coreference was detected  
        return coreferents
    
    def get_coref_type( self, upostag, feats): # -> Coref_type
        """ if the coreferent is relevant for us """
        upostag_ok  = False
        prontype_ok = False
        
        if ( upostag in [ "PRON", "DET" ] ):
            upostag_ok = True        
        features = feats.split( '|')        
        for feat in features:
            if ( "PronType" in feat ):
                values = feat.split( '=')[1].split( ',')
                for val in [ "Prs", "Rel", "Dem" ]:
                    if ( val in values ):
                        prontype_ok = True        
        if ( upostag_ok and prontype_ok ):
            return Coref_type.Pronoun
        
        if ( upostag == "VERB" ): # not all verbs represents a dropped pronoun, but herecome only such verbs
            return Coref_type.Dropped
        
        return Coref_type.Irrelevant
        
    
class Coref_type( Enum):
    Irrelevant = 0 # everything except
    Pronoun    = 1 # personal/relative/demonstrative pronouns or determiners
    Dropped    = 2 # verbs
    
class Eval_cluster_record: # represents a group of coreferents
    def __init__( self, cluster_id):
        self.cluster_id = cluster_id
        self.coref_ids = []        
    def add_coreferent( self, coref_id):
        self.coref_ids.append( coref_id)
class Eval_coref_record: # represents a corefering word
    def __init__( self, coref_id, cluster, drop_cluster, coref_type):        
        self.coref_id = coref_id
        self.cluster = cluster
        self.drop_cluster = drop_cluster
        self.coref_type = coref_type
        
if ( len( sys.argv) == 2 ):
    e = Conll_evaluator()
    e.evaluate_all( sys.argv[1])

