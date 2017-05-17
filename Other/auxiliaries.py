def get_interstring( string, left_limit, right_limit): # -> string
    """
    returns a substring between the first left limit character and the first right limit character (excluding them)
    """
    interstring = ""
    is_interstring = False
    for char in string:
        if ( char == left_limit and not is_interstring ):
            is_interstring = True
        elif ( char == right_limit and is_interstring ):
            return interstring      
        elif ( is_interstring ):
            interstring += char
    
def join_with_separator( list, separator): # -> string
    string = str( list[0])
    for i in list[1:]:
        string += separator
        string += str( i)
    return string

def transform_ID( word_ID_string):
    try:
        word_ID = int( word_ID_string)
        lines_to_omit = 0
    except:
        split = word_ID_string.split('-')
        if ( len( split) > 1 ):
            word_ID = int( split[0])
            word_ID_II = int( split[1])
            lines_to_omit = word_ID_II - word_ID + 1
        else:
            raise Exception( "Error in CoNLL-U!")
    return ( word_ID, lines_to_omit )