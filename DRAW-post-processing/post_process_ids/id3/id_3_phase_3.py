import tables
# import phase3_methods as methods
import lmrlib
# temperature values

def phase_3(entry):
    return_list = list(entry)
    value = entry[1]
    if value != '-999':
        try:
            value = '{:.2f}'.format(lmrlib.temp_f2c(float(value)))
        except ValueError:
            print ("Value error F to C: "+ entry[1])
            value = entry[1]
        except TypeError:
            value = entry[1]
            print ("Value error F to C: "+ entry[1])


    return_list[1] = value
    tables.add_to_final_corrected_table_iso(*return_list)
