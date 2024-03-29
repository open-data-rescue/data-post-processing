import tables
# import phase3_methods as methods
import lmrlib
#  id2 = vapour pressure


# transform to hPA
def phase_3(entry):
    return_list = list(entry)
    value = entry[1]
    if value != '-999':
        try:
            value = '{:.2f}'.format(lmrlib.baro_Eng_in2mb(value))
        except ValueError:
            value = entry[1]
        except TypeError:
            value = entry[1]

    return_list[1] = value
    tables.add_to_final_corrected_table_iso(*return_list)
