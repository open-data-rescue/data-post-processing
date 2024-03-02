import tables
# import phase3_methods as methods
import lmrlib
import string
#  id5 = direction

# transform to degrees
def phase_3(entry):
    return_list = list(entry)
    try:
        value = entry[1]
        v=float(value)
        if value != '-999':
            value = '{:<4}'.format(v)
            dc = 1
            imiss = -999
            value = '{:.2f}'.format(lmrlib.wind_4chardir2deg(value, dc, imiss))
    except ValueError:
        value = entry[1]
    except TypeError:
        value = entry[1]
    except KeyError:
        value='-999'

    return_list[1] = value
    tables.add_to_final_corrected_table_iso(*return_list)
