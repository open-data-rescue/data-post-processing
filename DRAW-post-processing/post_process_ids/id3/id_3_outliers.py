# This file fixes outliers for temperature values before moving on to next part of phase 2

import config
import tables


def patch_outlier(entry):
    value = entry[1]
    try:
        if str(value).lower() not in [*config.disregarded_values, 'none'] and \
        (float(value) < config.temperature_min or float(value) > config.temperature_max) and entry[10] == 0:
                original_value=value
                value='{:.1f}'.format(float(original_value)/10.0)
                tables.add_error_edit_code(2, '025', original_value, value, entry)
                return value

        else:
            return None
    except TypeError:
        pass
    except ValueError:
        pass