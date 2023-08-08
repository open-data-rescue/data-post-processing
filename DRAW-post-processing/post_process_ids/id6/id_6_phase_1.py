import phase1_methods as methods
import tables

def phase_1(entry):
    synonyms_empty = ('empty', 'illegible', 'retracted', 'emptyblank', 'blank')
    #single_letters = ('S', 's', 'T', 't', 'N', 'n') #things I noticed that appear by themselves
    inaps = ('inappreciable', '?napp', 'napp', 'inap', 'inapp')
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return_list = list(entry)
    value = entry[1]
    if value != None and value != '': #in case non-empty value
        value = value.lower()
        value = value.replace(' ','')
        if value in synonyms_empty: # only treat in case the data is purposely empty
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
                return None
        else:   
            
            if value in inaps: # to unify results
                value= 'inapp'
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
                return None
                
            if entry[4]==35 or entry[4]==48: #special treatment for field_id 35\48 as value is a number
                value = methods.remove_spaces(value, return_list)
                value = methods.correct_double_decimals(value, return_list)
                value = methods.remove_unexpected_characters(value, return_list)
                value = value.replace(";",".")
                for elements in value: # my way to remove alphabetical characters
                    if elements in alphabet:
                        value=value.replace(elements,'')
                    elif elements in alphabet.upper():
                        value=value.replace(elements,'')
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
                return None
            
            elif entry[4]==19: # bug sometimes two entries with same id. Only one id is transformed
                counter=0
                for elem in value: # if only numbers in a value where there should at least have a letter, put ?
                    if elem in alphabet or elem in alphabet.upper():
                        counter+=1
                if counter==0:
                    value='?'
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
                return None
                    
            elif entry[4]==34: # this entry is number
                value=value.replace('.','') # deal with double '.'
                if len(value)==3: # 123 becomes 1.23
                    value=value[0]+'.'+value[1:] 
                elif len(value)==4: # 1234 becomes 12.34
                    value=value[:2]+'.'+value[2:]
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
         
    elif value == None or value=='': # deal with empty values
        tables.add_to_corrected_table(*return_list, 0)
        return None