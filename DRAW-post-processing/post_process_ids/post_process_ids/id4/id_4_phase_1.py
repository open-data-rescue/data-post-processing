import phase1_methods as methods
import tables
#  id4 = precipitation amount


def phase_1(entry):
    '''
    Parameters
    ----------
    Returns
    -------
    None.

    ERROR CODE ARE NOT UPLOADED !!

    '''
    synonyms_empty = ('empty', 'illegible', 'retracted', 'emptyblank', 'blank')
#    single_letters = ('S', 's', 'T', 't', 'N', 'n', 'R', 'r') #things I noticed that appear by themselves
    inaps = ('inapp', 'inappreciable', 'inap', '?napp', 'napp','Inapp','r')
    return_list = list(entry)
    value = entry[1]
    if value == None or value == '':  # in case missing values
        tables.add_to_corrected_table(*return_list, 0)
        return None
    elif value.lower() in inaps:  # to unify inaps value
        value = 0.01
        return_list[1] = value
        tables.add_to_corrected_table(*return_list, 0)
        return None

    elif value.lower() in synonyms_empty:  # if the value was purposely put as problematic
        return_list[1] = value.lower()
        tables.add_to_corrected_table(*return_list, 0)
        return None

    else:  # Only deals with values with data in them
        value = value.lower()
        value = value.replace(' ', '')
        value = methods.remove_spaces(value, return_list)
        value = methods.correct_double_decimals(value, return_list)
        value = methods.remove_unexpected_characters(value, return_list)
        value = methods.remove_negatives(value, return_list)
        value = methods.remove_question(value, return_list)
        value = value.replace(";", ".")
        value = value.replace("'", '.')  # to deal with 3'2
#        value = value.replace('°','')
#        value = value.replace('~','')

        value = value.replace(',', '.')
        value = value.replace('/', '0')
        value = value.replace('-', '0')
        try:
            v = float(value)
            return_list[1] = value
            tables.add_to_corrected_table(*return_list, 0)
        except:
             tables.add_error_edit_code(1, '024', value, return_list[1], return_list)
        return None
