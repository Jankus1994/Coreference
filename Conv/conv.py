# Jan Faryad
# 12. 7. 2017

"""Classes for general processing of the original files - certain methods to be overloaded with specific ones"""

from udapi.core.block import Block
import re

class Conv_text_converter:
    """The main class for extraction of the plain text from anotated data"""
    def __init__( self, input_list_name, output_list_name):
        input_list = open( input_list_name, 'r')
        output_list = open( output_list_name, 'r')
        for input_file_name in input_list:
            output_file_name = output_list.readline()
            
            input_file = open( input_file_name[:-1], 'r')
            output_file = open( output_file_name[:-1], 'w')
            self.convert_file( input_file, output_file)
            input_file.close()
            output_file.close()
            
        input_list.close()
        output_list.close()
    
    def convert_file( self, input_file, output_file):
        pass

class Conv_coref( Block):
    """
    General parent class for more specific convertors of corefeernce information from the original data to ConLL-U files
    defines a few components which the inherited classes must meet
    """    
    def __init__( self, **kwargs):
        #super( Conv_main, self).__init__()
        super().__init__( **kwargs)
        self.word_correspondence  = Conv_word_correspondence()
        self.coreference_getter   = Conv_coreference_getter()
        self.word_converter       = Conv_word_converter()
        self.coreference_setter   = Conv_coreference_setter()
    
    def process_document( self, document):
        
        path = "../coreference/" # the actual folder is udapi-python/udapi
        name = re.sub( r'([^\.]*).*', r'\1', document.filename) # filename exept the suffix (to the first dot, excluding)
        full_name = path + name
        
        # building a matching between word ids and udapi nodes
        list_of_corresponding_words = self.word_correspondence.execute( full_name, document)
        
        # extracting information about coreference from
        list_of_coreferents = self.coreference_getter.execute( full_name)        
        
        # conversion of the coreferents' ids to nodes
        list_of_coreferents = self.word_converter.execute( list_of_coreferents, list_of_corresponding_words)

        # adding the coreference information into the CoNLL-U file    
        self.coreference_setter.execute( list_of_coreferents) # document is not needed, nodes are in the corespondence list
        
        #super().process_document( document)
        
    def process_node( self, node):
        """
        the only proper general proccesing section - normailzation of coreference of coordinated structuers:
        in UD the first conjunct is the haed of the structure, so the information is written here - although then it is not clear wheather the coreferent is the first conjunct only or the whle structure
        in some corpora, the is the conunction considered as the head - then we have to rewrite the coreference from the conjunction to the first conjunct
        this could be done generally, independently of the original data
        """
        coref = node.misc[ "Coref" ]
        drop_coref = node.misc[ "Drop_coref" ]
        if ( ( coref or drop_coref ) and  "cc" in node.deprel ): # conjunction with a coreference information
            parent = node.parent # the last conjunct typically
            if ( node.parent.deprel == "conj" ):
                grandparent = parent.parent  # the first conjunct            
                if ( coref ):
                    del( node.misc[ "Coref" ])
                    grandparent.misc[ "Coref"] = coref
                if ( drop_coref ):
                    del( node.misc[ "Drop_coref" ])
                    grandparent.misc[ "Drop_coref"] = drop_coref                        

# classes working with the original data - to be overloaded with specific classes for a particular corpus

class Conv_word_correspondence:
    def execute( self):
        return

class Conv_coreference_getter:
    def execute( self):
        return

class Conv_word_converter:
    def execute( self):
        return

class Conv_coreference_setter:
    def execute( self):
        return
