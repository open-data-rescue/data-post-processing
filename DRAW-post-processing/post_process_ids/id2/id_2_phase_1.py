import phase1_methods as methods
import tables
#  id2 = vapour pressure


def phase_1(entry):
    '''
    Parameters
    ----------

    Returns
    -------
    None.

    ERROR CODE ARE NOT UPLOADED !!
    '''

# check value >0
# if value >2, divide by 1000

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    synonyms_empty = ('empty', 'illegible', 'retracted', 'emptyblank', 'blank')
#    single_letters = ('S', 's', 'T', 't', 'N', 'n', 'R', 'r') #things I noticed that appear by themselves
    inaps = ('inapp', 'inappreciable', 'inap', '?napp', 'napp')
    return_list = list(entry)
    value = entry[1]

    if value == None or value == '':  # in case missing values
        tables.add_to_corrected_table(*return_list, 0)
        return None
    elif value.lower() in inaps:  # to unify inaps value
        value = 'inapp'
        return_list[1] = value.lower()
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
        value = value.replace("-", "")  # remove any negative signs
        value = value.replace(";", ".")
        value = value.replace("'", '.')  # to deal with 3'2
#        value = value.replace('°','')
#        value = value.replace('~','')
        for elements in value:  # my way to remove alphabetical characters
            if elements in alphabet:
                value = value.replace(elements, '')
            elif elements in alphabet.upper():
                value = value.replace(elements, '')

        value = value.replace(',', '.')
        value = value.replace('/', '0')
        value = value.replace('-', '0')
        if len(value) > 0:
            if value[0] == '.':  # to avoid .6 and put 0.6
                value = '0' + value
            if value[-1] == '.':  # to avoid 6. and put 6.0
                value = value+'0'
        return_list[1] = value
        tables.add_to_corrected_table(*return_list, 0)
        return None
