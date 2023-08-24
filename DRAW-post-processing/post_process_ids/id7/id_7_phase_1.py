import phase1_methods as methods
import tables

def phase_1(entry):

    return_list = list(entry)
    value = entry[1]
    synonyms_empty = ('empty', 'illegible', 'retracted', 'emptyblank', 'blank')
   # single_letters = ('S', 's', 'T', 't', 'N', 'n') #things I noticed that appear by themselves
    inaps = ('inappreciable', '?napp', 'napp', 'inap', 'inapp')
    
    if value != None and value != '': # deal with non-empty entries
        value = value.lower()
    
        if value in synonyms_empty: #if value purposely left empty
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
                return None
        else:
            if value in inaps: # to unify values
                value= 'inapp'
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
                return None
            else: # general formatting
                value = methods.remove_spaces(value, return_list)
                value = methods.correct_double_decimals(value, return_list)
                value = methods.remove_unexpected_characters(value, return_list)
                value = value.replace(";",".")
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
                return None

    elif value == None or value=='': # deal with empty entries
        tables.add_to_corrected_table(*return_list, 0)
        return None