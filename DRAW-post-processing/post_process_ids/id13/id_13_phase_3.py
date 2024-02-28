import tables
import phase3_methods as methods
# id3 = distance (miles), eg distance wind has run


def phase_3(entry):
    return_list = list(entry)
    value = entry[1]
    if value != '-999':
        try:
            v=float(value)/3600.0
            value = '{:.2f}'.format((methods.dis_mi2m(v)))
            if entry[4] == 35:
                value = value / (3.0)
            elif entry[4] == 48:
                value = value / (24.0)
        except ValueError:
            value = entry[1]
        except TypeError:
            value = entry[1]

    return_list[1] = value
    tables.add_to_final_corrected_table_iso(*return_list)
