# file where all important MySQL commands are kept, or created during runtime (see methods)


composite_raw_data_entries = "CREATE TABLE IF NOT EXISTS data_entries_raw AS SELECT " \
                             \
                             "data_entries.id, " \
                             "data_entries.value, " \
                             "data_entries.user_id, " \
                             "data_entries.page_id, " \
                             "data_entries.field_id, " \
                             "fields.field_key, " \
                             "data_entries.annotation_id, " \
                             "annotations.transcription_id, " \
                             "fields.post_process_id, " \
                             "annotations.observation_date " \
                             \
                             "FROM data_entries " \
                             "LEFT JOIN fields " \
                             "ON fields.id = data_entries.field_id " \
                             "LEFT JOIN annotations " \
                             "ON data_entries.annotation_id = annotations.id "\
                             "WHERE fields.post_process_id IS NOT NULL;"


composite_raw_data_entries_continue = "CREATE TABLE IF NOT EXISTS data_entries_raw AS SELECT " \
                             \
                             "data_entries.id, " \
                             "data_entries.value, " \
                             "data_entries.user_id, " \
                             "data_entries.page_id, " \
                             "data_entries.field_id, " \
                             "fields.field_key, " \
                             "data_entries.annotation_id, " \
                             "annotations.transcription_id, " \
                             "fields.post_process_id, " \
                             "annotations.observation_date " \
                             \
                             "FROM data_entries " \
                             "LEFT JOIN fields " \
                             "ON fields.id = data_entries.field_id " \
                             "LEFT JOIN annotations " \
                             "ON data_entries.annotation_id = annotations.id "\
                             "WHERE fields.post_process_id IS NOT NULL AND " \
                             "data_entries.id not in (select id from data_entries_corrected_final);"


def create_error_edit_table(phase):
    error_edit_code_table = "CREATE TABLE data_entries_phase_{}_errors (" \
                                "id INT, " \
                                "ORIGINAL_VALUE TEXT, " \
                                "CORRECTED_VALUE TEXT, " \
                                "error_code VARCHAR(4) NOT NULL, " \
                                "user_id INT, " \
                                "page_id INT, " \
                                "field_id INT, " \
                                "field_key VARCHAR(255), " \
                                "annotation_id INT, " \
                                "transcription_id INT, " \
                                "post_process_id INT, " \
                                "observation_date DATETIME, " \
                                "additional_info TEXT" \
                            ");".format(phase)
    return error_edit_code_table


raw_data_sql = "SELECT * FROM data_entries_raw;"

phase_1_data_sql = "SELECT * FROM data_entries_corrected_duplicateless;"
phase_1_data_test_sql = "SELECT * FROM data_entries_corrected_duplicateless_test;"


# MySQL commands used during post-processing phases:

# retrieves entries from same annotation in method "reference_previous_values" (PHASE 1)
def check_1_command(entry):
    annotation_id = entry[6]
    return raw_data_sql[:len(raw_data_sql) - 1] + " WHERE annotation_id = {} ORDER BY observation_date desc".format(annotation_id)


# retrieves entries from same/previous day in same relevant field group in method "reference_previous_values" (PHASE 1)
def check_2_command(entry, counter):
    try:
 #       observation_date = entry[9] - datetime.timedelta(days=counter)
         observation_date = entry[9]
         if observation_date is None:
             return -1
    except TypeError:
        return -1
    field_id = entry[4]
    if field_id in [4, 6, 7]:
        return raw_data_sql[:len(raw_data_sql) - 1] + " WHERE field_id IN (4,6,7) " \
                                                      "AND observation_date >= '{}'".format(str(observation_date)[:10]) + \
                                                      " - INTERVAL 25 DAY AND observation_date <'{}'".format(str(observation_date)[:10]) + \
                                                          " ORDER BY observation_date DESC"
    if field_id == 8:
        return raw_data_sql[:len(raw_data_sql) - 1] + " WHERE field_id IN (4,6,7,8) " \
                                                      "AND observation_date >= '{}'".format(str(observation_date)[:10]) + \
                                                      " - INTERVAL 25 DAY AND observation_date <'{}'".format(str(observation_date)[:10]) + \
                                                          " ORDER BY observation_date DESC"
    if field_id in [67, 69]:
        return raw_data_sql[:len(raw_data_sql) - 1] + " WHERE field_id IN (67,69) " \
                                                      "AND observation_date >= '{}'".format(str(observation_date)[:10]) + \
                                                      " - INTERVAL 25 DAY AND observation_date <'{}'".format(str(observation_date)[:10]) + \
                                                          " ORDER BY observation_date DESC"

# finds value for same field_id and up one row in the ledger sheet (i.e. in the previous timestamp) (PHASE 2)
def ref_adjacent_fluctuations(entry, obs_datetime):
    field_id = entry[4]
    return phase_1_data_sql[:len(phase_1_data_sql) - 1] + " WHERE field_id = {} " \
                                                          "AND observation_date LIKE '{}%';".format(field_id, str(obs_datetime)[:10])


# retrieves relevant field_id's in ledger sheet, to calculate particular field_id based on other two elements, using equation 1, 2 oe 3 (PHASE 2)
def equation_retrieve_row(entry, equation_num):
    field_ids = None
    match equation_num:
        case 1:
            field_ids = (4, 5, 6)  # to find field_id = 7
        case 2:
            field_ids = (4, 6, 7, 9, 10)  # to find field_id = 8
        case 3:
            field_ids = (5, 7)  # to find field_id = 6
    observation_date = str(entry[9])
    return phase_1_data_sql[:len(phase_1_data_sql) - 1] + " WHERE observation_date = '{}' " \
                                                          "AND field_id IN {};".format(observation_date, field_ids)
