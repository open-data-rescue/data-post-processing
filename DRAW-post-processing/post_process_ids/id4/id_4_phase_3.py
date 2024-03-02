import tables
import phase3_methods as methods
#  id4 = precipitation amount


# transform to mm
def phase_3(entry):
    return_list = list(entry)
    value = entry[1]
    try:
        v=float(value)
        value = '{:.2f}'.format(methods.depth_in2mm(v))
    except ValueError:
        value = entry[1]
    except TypeError:
        value = entry[1]

    return_list[1] = value
    tables.add_to_final_corrected_table_iso(*return_list)
