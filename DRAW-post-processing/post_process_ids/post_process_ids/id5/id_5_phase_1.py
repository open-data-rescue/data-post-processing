import phase1_methods as methods
import tables
#  id5 = direction


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
    synonyms_empty = ('empty', 'illegible', 'retracted', 'emptyblank', 'blank')
#    single_letters = ('S', 's', 'T', 't', 'N', 'n') #things I noticed that appear by themselves
    inaps = ('inappreciable', '?napp', 'napp', 'inap', 'inapp')
    if value != None and value != '':  # in case non-empty values
        value = value.lower()
        value = value.replace(' ', '')
        if (str.isalpha, value) == 'True':
            if value in synonyms_empty:  # only treat in case the data is empty
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
            elif value == None or value == '':  # in case empty values
                return None
            else:  # value not empty
                if value in inaps:  # to unify results that are inaps
                    value = 'inapp'
                    return_list[1] = value
                    tables.add_to_corrected_table(*return_list, 0)
                    return None
                else:  # deals with the rest of field ids
                    value = methods.remove_spaces(value, return_list)
                    value = methods.remove_question(value, return_list)
                    value = value.replace(";", ".")
                    return_list[1] = value
                    tables.add_to_corrected_table(*return_list, 0)
            return None
    else:
        tables.add_error_edit_code(1, '025', value, return_list[1], return_list)
