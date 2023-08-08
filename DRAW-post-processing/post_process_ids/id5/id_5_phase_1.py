import phase1_methods as methods
import tables

def phase_1(entry):
    '''
    

    Parameters
    ----------
    entry : TYPE
        What to do if value is a string, but only has a number

    Returns
    -------
    None.

    '''
    return_list = list(entry)
    value = entry[1]
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    synonyms_empty = ('empty', 'illegible', 'retracted', 'emptyblank', 'blank')
    #single_letters = ('S', 's', 'T', 't', 'N', 'n') #things I noticed that appear by themselves
    inaps = ('inappreciable', '?napp', 'napp', 'inap', 'inapp')
    if value != None and value != '': #in case non-empty values
        value = value.lower()
        value = value.replace(' ','')
        if value in synonyms_empty:  # only treat in case the data is empty
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
                return None
        else: # value not empty
            if value in inaps: # to unify results that are inaps
                value= 'inapp' 
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
                return None
                
            if entry[4]==24:  # special treatment for field_id 24 as value is a number
                value = methods.remove_spaces(value, return_list)
                value = methods.correct_double_decimals(value, return_list)
                value = methods.remove_unexpected_characters(value, return_list)
                value = value.replace(";",".")
                for elements in value: # my way to remove alphabetical characters
                    if elements in alphabet:
                        value=value.replace(elements,'')
                    elif elements in alphabet.upper():
                        value=value.replace(elements,'')
                        
            else: #deals with the rest of field ids
                value = methods.remove_spaces(value, return_list)
                value = methods.correct_double_decimals(value, return_list)
                value = methods.remove_unexpected_characters(value, return_list)
                value = value.replace(";",".")  
                counter=0
                for elem in value: # if only numbers in a value where there should at least have a letter, put ?
                    if elem in alphabet or elem in alphabet.upper():
                        counter+=1
                if counter==0:
                    value='?'
                          
        return_list[1] = value
        tables.add_to_corrected_table(*return_list, 0)
        return None
    
    elif value == None or value=='': #in case empty values
        tables.add_to_corrected_table(*return_list, 0)
        return None