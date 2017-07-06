# Jan Faryad
# 20. 4. 2017
#
# processing a conll-u document for obtaining data for feature vectors easily

from conll_node import Node

class CoNLL_processor:
    def __init__( self, input):
        self.input = input
    def process_document( self):
        document = Document()
        para_id = 0
        actual_sentence = Sentence( 0, None) # so that it's existence needn't be controlled
        for line in self.input:
            if ( line[0] == '#' ): # comment line beginning with #
                fields = line.split( '\t')
                if ( len( fields) == 4 and fields[1] == '$' ): # new sentence with paragraph and sentence id
                    new_para_id = int( fields[2])
                    if ( para_id != new_para_id ): # new paragraph
                        para_id = new_para_id
                        actual_paragraph = Paragraph( para_id, document)
                        document.paragraphs.append( actual_paragraph)
                    actual_sentence.finalize() # things that can be done only after creation of all nodes
                    sent_id = int( fields[3])
                    actual_sentence = Sentence( sent_id, actual_paragraph)
                    actual_paragraph.add_sentence(actual_sentence)
            elif ( line != ' \n' ): # not a blank line -> record line
                node = Node( actual_sentence, line)
                actual_sentence.add_node( node)
        return document
class Document:
    """
    root object of the whole processed document, contains paragraphs
    """
    def __init__( self):
        self.paragraphs = []
    def add_paragraph( self, paragraph): # void
        self.paragraphs.append( paragraph)
class Paragraph:
    """
    children of document, contain sentences
    """
    def __init__( self, number, document):
        self.number = number
        self.sentences = []
        self.document = document
    def add_sentence( self, sentence): # void
        self.sentences.append( sentence)
class Sentence:
    """
    children of paragraphs, contain nodes
    """
    def __init__( self, number, paragraph):
        self.number = number
        self.nodes = []
        self.paragraph = paragraph
        self.root = None
        self.depth = 0
        self.nodes_number = 0
    def add_node( self, node): # void
        self.nodes.append( node)
    def get_node_by_id( self, id): # -> Node
        """
        used by getting a head of a node by head id
        called from head and deps setting, see node file
        """
        if ( id == 0 or id == -1 ): # root and range nodes don't have a head - root has head_id = 0, range nodes -1,
                                    # but there's no node with id = 0
            return None
        for node in self.nodes: # it has to be searched, because there could be also range nodes, so index in list != node id
            if ( node.id == id ):
                return node
        for node in self.nodes: # if there isn't an exact node, only a range node
            if ( node.id_range[0] <= id and  node.id_range[1] >= id ):
                return node
    def set_root( self, node): # void
        """
        called by the root itself, see node file
        """
        self.root = node
    def finalize( self): # void
        """
        things that can be done only after creation of all nodes
        
        creates pointers to heads (both primary and secondary) of all nodes - up to now there were only head ids
        sets node depths and paths recursively from root
        sets sentence depth and number of nodes
        """
        for node in self.nodes:  # heads
            node.set_head()
            node.set_deps()        
        if ( self.root != None ): # depths and paths
            self.root.set_depth_and_path( 0, []) # root's "head" has depth = 0 and and empty path
        
        for node in self.nodes:
            if ( node.depth > self.depth ): # depth of the sentence = maximum node depth
                self.depth = node.depth
            if ( node.id > self.nodes_number ): # number of real nodes in the sentence - not range nodes
                self.nodes_number = node.id 
        
        
        
        
        
        
        
        
        
        
        
