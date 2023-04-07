import tables
import phase3_methods as methods

def phase_3(entry):
    return_list = list(entry)
    value = entry[1]
    if value!='-999':
        try:
            value = '{:.2f}'.format(methods.temp_f2c(value))
        except ValueError:
            value=entry[1]
        except TypeError:
            value=entry[1]

    return_list[1] = value
    tables.add_to_final_corrected_table_iso(*return_list)
