import phase1_methods as methods
import tables
#  id 6 = velocity


def phase_1(entry):
    synonyms_empty = ('empty', 'illegible', 'retracted', 'emptyblank', 'blank')
#    single_letters = ('S', 's', 'T', 't', 'N', 'n') #things I noticed that appear by themselves
    inaps = ('inappreciable', '?napp', 'napp', 'inap', 'inapp')
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return_list = list(entry)
    value = entry[1]
    if value != None and value != '':  # in case non-empty value
        value = value.lower()
        value = value.replace(' ', '')
        if value in synonyms_empty:  # only treat in case the data is purposely empty
            return_list[1] = value
            tables.add_to_corrected_table(*return_list, 0)
            return None
        else:
            if value in inaps:  # to unify results
                value = 'inapp'
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
                return None
            else:
                value = methods.remove_spaces(value, return_list)
                value = methods.correct_double_decimals(value, return_list)
                value = methods.remove_unexpected_characters(value, return_list)
                value = methods.remove_negatives(value, return_list)
                value = methods.remove_question(value, return_list)
                value = value.replace('.', '')  # deal with double '.'
                value = value.replace(";", ".")
                for elements in value:  # my way to remove alphabetical characters
                    if elements in alphabet:
                        value = value.replace(elements, '')
                    elif elements in alphabet.upper():
                        value = value.replace(elements, '')
                return_list[1] = value
                try:
                    v=float(value)
                    return_list[1]=value
                    tables.add_to_corrected_table(*return_list, 0)
                except ValueError:
                    tables.add_error_edit_code(1, '024', value, return_list[1], return_list)
                return None
    elif value == None or value == '':  # deal with empty values
        return_list[1]='empty'
        tables.add_to_corrected_table(*return_list, 0)
        return None
