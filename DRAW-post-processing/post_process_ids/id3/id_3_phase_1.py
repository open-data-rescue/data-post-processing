# post-processing format check algorithm for post_process_id = 3

import tables
import phase1_methods as methods




def phase_1(entry):
    return_list = list(entry)
    value = entry[1]

    # Checking to see if raw pressure value is already of form XX.XXX
    if methods.desired_temperature_format(value):
        tables.add_to_corrected_table(*return_list, 0)

    elif methods.disregarded_value(value):
        tables.add_to_corrected_table(*return_list, 0)

    elif value is None:
        tables.add_to_corrected_table(*return_list, 0)
    
    elif "dry" in value.lower() or "frozen" in value.lower():
        value=methods.extract_decimal(value, return_list)
        tables.add_to_corrected_table(*return_list, 0)

    # if not of the right form initially, corrects format and returns entry with corrected value
    else:

        value = methods.remove_spaces(value, return_list)
        value = methods.correct_double_decimals(value, return_list)
        value = methods.remove_alphabetical_char(value, return_list)
        value = methods.remove_unexpected_characters(value, return_list)
        value = value.replace(";",".")

        return_list[1] = value
        if methods.desired_temperature_format(value):
            tables.add_to_corrected_table(*return_list, 0)