# File for configuring variables/attributes that are addressed in the workflow

import phase1_methods as methods

# assigning post-process ID's to field ID's
# assign a TUPLE to multiple field_id's with one PPID; otherwise assign integer for single field_id
# 1: pressure(in_hg), 2: vapour pressure(in_Hg), 3:temperature (F), 4: precipitation (in), 5: direction, 6: velocity (miles), 7: weather, 8: cloud type, 9:time, 10: RH (%), 11: cloud cover (tenths), 12 :various (character)
ppid_to_field_id = {1: (4, 6, 7, 8, 67, 69),
                    2: 14,
                    3: (5, 9, 10, 11, 12, 13, 33, 36, 37, 38, 39, 62, 63, 64, 68, 76, 77, 78, 79, 81),
                    4: (27, 30, 31, 50),
                    5: (17, 19, 23),
                    6: (20),
                    7: (18, 40, 41, 44, 51, 52, 56, 57, 66, 80, 82, 83),
                    8: (16, 22, 53, 54),
                    9: (25, 26, 28, 29, 46, 65, 70, 71),
                    10: (15, 58, 59, 60, 72, 74, 75),
                    11: (24),
                    12: (21, 61, 42, 47, 66),
                    13: (34, 35, 48)}

sef_type_to_field_id = {"atb": (5, 68),
                        "au": (47),
                        "cl": (22, 53),
                        "cd": (23),
                        "ch": (16, 54),
                        "dd": (19),
                        "e": (14),
                        "hd": (17),
                        "mslp": (7),
                        "nl": (24),
                        "p": (4, 67),
                        "p_cor": (7, 69),
                        "pr": (27, 31),
                        "ptb": (25, 28),
                        "pte": (26, 29),
                        "rh": (15, 58, 59, 73, 75, 60, 72),
                        "rrt": (66),
                        "sd": (50),
                        "rain_dur": (70),
                        "snow_dur": (71),
                        "ss": (65),
                        "ta": (9),
                        "ta_cor": (10),
                        "tb": (11),
                        "tb_cor": (12),
                        "td": (33),
                        "TGn": (62, 81),
                        "Tn": (38, 76),
                        "Tn_cor": (37, 77),
                        "Tx": (36, 78),
                        "Tx_cor": (37, 79),
                        "Tsx": (63, 64),
                        "wf": (85),
                        "w": (34, 48, 35),
                        "ws": (20),
                        "ww": (18, 52, 40, 44, 57, 56, 80, 83),
                        "w2": (51, 41, 82)
                        }
sef_type_to_unit={"atb": "C",
                       "au": "text",
                       "cl":"lct",
                       "cd":"dir",
                       "ch":"uct",
                       "dd":"dir",
                       "e":"hPa",
                       "hd":"dir",
                       "mslp":"hPa",
                       "nl":"okta",
                       "p": "hPa",
                       "p_cor":"hPa",
                       "pr":"mm",
                       "ptb":"hr",
                       "pte":"hr",
                       "rh":"p",
                       "rrt":"text",
                       "sd":"mm",
                       "rain_dur":"hh:mm",
                       "snow_dur":"hh:mm",
                       "ss":"mm",
                       "ta":"C",
                       "ta_cor":"C",
                       "tb":"C",
                       "tb_cor":"C",
                       "td":"C",
                       "TGn":"C",
                       "Tn":"C",
                       "Tn_cor":"C",
                       "Tx":"C",
                       "Tx_cor":"C",
                       "Tsx":"C",
                       "wf":"?",
                       "w":"miles",
                       "ws":"mph",
                       "ww":"mno",
                       "w2":"mno"
                       }
sef_type_to_start={"atb": "stat",
                       "au": "stat",
                       "cl":"stat",
                       "cd":"stat",
                       "ch":"stat",
                       "dd":"stat",
                       "e":"stat",
                       "hd":"stat",
                       "mslp":"stat",
                       "nl":"stat",
                       "p": "stat",
                       "p_cor":"stat",
                       "pr":"stat",
                       "ptb":"stat",
                       "pte":"stat",
                       "rh":"stat",
                       "rrt":"stat",
                       "sd":"stat",
                       "rain_dur":"stat",
                       "snow_dur":"stat",
                       "ss":"stat",
                       "ta":"stat",
                       "ta_cor":"stat",
                       "tb":"stat",
                       "tb_cor":"stat",
                       "td":"stat",
                       "TGn":"stat",
                       "Tn":"stat",
                       "Tn_cor":"stat",
                       "Tx":"stat",
                       "Tx_cor":"stat",
                       "Tsx":"stat",
                       "wf":"stat",
                       "w":"stat",
                       "ws":"stat",
                       "ww":"stat",
                       "w2":"stat"
                       }
sef_apply_utc=False
sef_utc_offset=5

# look at 27 for inap
# unexpected characters in a data entry (when not surrounded on either side by digits)  TODO : determine if any alterations necessary for non-pressure values
unexpected_characters = {'?', '.', '*', '&', '#', '^', '$', '(', ')', '[', ']', '{', '}', '"', '/', '@', "\\", ';'}


# characters that could potentially have replaced decimal point in a numerical data entry
decimal_point_alternates = {';', '-', '/', ','}


# values that can be disregarded automatically; method converts all data entries to lowercase to catch edge cases where term is capitalized or uncapitalized irregularly
disregarded_values = {'empty', 'blank', 'retracted', 'empty / blank', 'vide', 'none existant', 'illegible', ''}


# possible leading digits for a pressure value:
possible_lead_digits_pressure = {'28', '29', '30', '31'}


# possible correct formats that a value can be in, for cases where we want to retrieve leading digits from it (True) or use the whole value (False):
def possible_pressure_formats(value, for_leading_digits):
    if methods.desired_pressure_format(value):
        return True
    elif len(value) in [5, 6, 7, 8] and methods.float_decimal_index(value) == 2:
        return True
    elif for_leading_digits:
        if len(value) == 5 and value.isnumeric():
            return True


# outlier bounds for pressure values
pressure_min = 27.000
pressure_max = 33.000

# outlier bounds for temperature values

temperature_min = -100.0
temperature_max=  {
    "5": 100,
    "9": 120,
    "10": 120,
    "11": 110,
    "12": 110,
    "13": 110,
    "33": 130,
    "36": 130,
    "37": 130,
    "38": 100,
    "39": 100,
    "62": 130,
    "63": 160,
    "64": 160,
    "68": 100,
    "76": 100,
    "77": 100,
    "78": 130,
    "79": 130,
    "81": 130
}



# temperature difference allowed
temperature_difference_allowed_obs_corr=2

# temperature corresponding fields observed - corrected
temperature_corr_observed_fields=[[9,10],[11,12],[36,37],[38,39],[76,77],[78,79]]
temperature_min_max_fields=[[38,36],[39,37],[76,78],[77,79],[81,76],[81,77],[81,38],[81,39],[62,76],[62,77],[62,38],[62,39]]

##TODO
temperature_less_than_other_fields=[[11,[9]],[12,[10]],[33,[9,10]]] # first field to compare to rest of the list - same observation time
temperature_min_fields=[[38,9],[39,10],[76,9],[77,10]] # check that the first field is <= to past 24 hours of other field
temperature_max_fields=[[36,9],[37,10],[78,9],[78,10]] # check that the first field is <= to past 24 hours of other field

temperature_air_wet_bulb_threshold=15
temperature_air_wet_bulb=[[9,11,13],[10,12,13]] #same observation time: abs(abs(field[0]-field[1])-abs(field[2]))<air_wet_bulb_threshold

# temperature fields to detect stat outliers
temperature_stat_outliers=[9,10]

#define whether to display or not graphs for outliers
temperature_plot_outliers=False
temperature_outlier_std_factor=5

# threshold value for which fluctuation between previous timestamp and current timestamp (for same field id) requires further investigation (phase 2)
scalar_fluctuation_thresholds = {'01': 0.30, '02': 0.40, '03': 0.50, '04': 0.50, '05': 0.50, '06': 0.50,  # TODO : fill w/ pressure_fluctuation_stats results
                                 '07': 0.60, '08': 0.60, '09': 0.60, '10': 0.70, '11': 0.80, '12': 0.80}

# amount of time (in hours) between timestamps, for which a pressure fluctuation isn't granular enough
time_delta_limit = 12  # TODO : change to 3

# threshold value for which difference between transcribed and equation value requires further investigation (phase 2)
pressure_diff_threshold = 0.300


# intervals of interest for difference between transcribed and equation value - used for discerning values whose leading digits have (likely) been added incorrectly,
# hence the intervals occurring at +/- 1 range; configure the floats in the conditional statements according to your own statistical results (see stat_test_equations.py)
def possible_wrong_lead_digs_id_4(difference_value):  # TODO : fill in with same interval stats as other field id's below
    try:
        difference_value = float(difference_value)
        if -999999999 <= difference_value <= -999999999:
            return 'is_left'
        elif -999999999 <= difference_value <= 999999999:
            return 'is_right'
        else:
            return False
    except TypeError:
        return False


def possible_wrong_lead_digs_id_6(difference_value):
    try:
        difference_value = float(difference_value)
        if -1.015 <= difference_value <= -0.997:
            return 'is_left'
        elif 0.997 <= difference_value <= 1.015:
            return 'is_right'
        else:
            return False
    except TypeError:
        return False


def possible_wrong_lead_digs_id_7(difference_value):
    try:
        difference_value = float(difference_value)
        if -1.005 <= difference_value <= -0.995:
            return 'is_left'
        elif 0.995 <= difference_value <= 1.005:
            return 'is_right'
        else:
            return False
    except TypeError:
        return False


def possible_wrong_lead_digs_id_8(difference_value):
    try:
        difference_value = float(difference_value)
        if -1.200 <= difference_value <= -0.900:
            return 'is_left'
        elif 0.900 <= difference_value <= 1.200:
            return 'is_right'
        else:
            return False
    except TypeError:
        return False
