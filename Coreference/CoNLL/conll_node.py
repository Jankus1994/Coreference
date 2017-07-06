# Jan Faryad
# 20. 4. 2017
#
# node class of processor has it's own file

class Node:
    def __init__( self, sentence, record_line):
        self.sentence = sentence
        self.process_record_line( record_line)        
        self.subnodes = []
        self.depth = -1 # remains to be set -1 for auxiliary nodes such as range nodes, which are not included in the tree
        self.root_path = []
    def process_record_line( self, record_line):
        if ( record_line[-1] == '\n' ):
            record_line = record_line[:-1]
        fields = record_line.split( '\t')
        #if ( len(fields) < 10 ):
        #    print(record_line)
        self.set_id( fields[0]) # each record line should have 10 fields
        self.set_form( fields[1])
        self.set_lemma( fields[2])
        self.set_upostag( fields[3])
        self.set_xpostag( fields[4])
        self.set_feats( fields[5])
        self.set_head_number( fields[6]) # only a number, pointer wil be set after processing of all sentence nodes
        self.set_deprel( fields[7])
        self.set_deps_numbers( fields[8]) # the same as for head
        self.set_misc( fields[9])
    def set_id( self, id_string):
        try:
            self.id = int( id_string)
            self.id_range = ( self.id, self.id)
        except:
            self.id = -1
            range = id_string.split( '-')
            if ( len( range) == 2 ): # range nodes
                try:
                    self.id_range = ( int( range[0]), int( range[1]) )
                except:
                    self.id_range = ( -1, -1)
    def set_form( self, form):
        self.form = form
    def set_lemma( self, lemma):
        self.lemma = lemma
    def set_upostag( self, upostag):
        self.upostag = upostag
    def set_xpostag( self, xpostag):
        self.xpostag = xpostag
    def set_feats( self, feats):                   
        self.feats = [] # list of features
        if ( feats == "_" ):
            return
        split_feats = feats.split( '|')
        for feat in split_feats:
            split_feat = feat.split( '=')
            name = split_feat[0]
            values = split_feat[1].split( ',') # there can be more values for one feature
            feature = ( name, values)
            self.feats.append( feature)
    def set_head_number( self, head):
        if ( head == "_"):
            self.head_number = -1 # for range nodes
        else:
            self.head_number = int( head)
            if ( self.head_number == 0 ): # root
                self.sentence.set_root( self)
    def set_head( self):
        """
        called after creation of all nodes in a sentence
        creates a pointer to head node according to head number and add this node to its head's list of subnodes
        """
        self.head = self.sentence.get_node_by_id( self.head_number) # None for root and range nodes
        if ( self.head != None):
            self.head.add_subnode( self) 
    def set_deprel( self, deprel):
        self.deprel = deprel
    def set_deps_numbers( self, deps):
        """
        deps ... secondary dependencies
        """
        self.deps = []
        if ( deps == "_" ):
            return        
        split_deps = deps.split( '|')
        for dep in split_deps:
            split_dep = dep.split( ':') # deps have for node_id:dep_name
            s_head_number = int( split_dep[0]) # only a number, not an object, for now
            s_deprel = split_dep[1]
            s_dependency = ( s_head_number, s_deprel)
            self.deps.append( s_dependency)
    def set_deps( self):
        """
        called after creation of all nodes in a sentence
        creates pointers to secondary heads in form ( sec_head_pointer, dep_name )
        """
        new_deps = []
        for pair in self.deps:
            s_head = self.sentence.get_node_by_id( pair[0])
            s_dependency = ( s_head, pair[1])
            new_deps.append( s_dependency)
        self.deps = new_deps         
    def set_misc( self, misc):
        """
        any other information
        here will be marked the coreference
        """
        self.misc = []
        if ( misc == "_" ):
            return
        split_misc = misc.split( '|')
        for misc in split_misc:
            split_misc = misc.split( '=')
            name = split_misc[0]            
            value = split_misc[1]
            miscellaneous = ( name, value)
            self.misc.append( miscellaneous)
    def set_depth_and_path( self, head_depth, root_path):
        """
        called after setting of heads and subnodes
        sets depths and root paths of nodes recursively
        """
        self.depth = head_depth + 1 # increasing the depth
        self.root_path = root_path + [ self ] # expanding the path
        for subnode in self.subnodes:
            subnode.set_depth_and_path( self.depth, self.root_path) # recursion
    def add_subnode( self, subnode): # void
        """
        called from subnode itself, when setting its head (= this node)
        """
        self.subnodes.append( subnode)
