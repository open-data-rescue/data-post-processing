import tables
# import phase3_methods as methods
import lmrlib
# id 11 = cloud cover (tenths)


def phase_3(entry):
    return_list = list(entry)
    value = entry[1]
    if value != '-999':
        try:
            v=float(value)
            value = '{:.1f}'.format(lmrlib.cloud_tenthscovered2oktas(v))
        except ValueError:
            value = entry[1]
        except TypeError:
            value = entry[1]

    return_list[1] = value
    tables.add_to_final_corrected_table_iso(*return_list)
