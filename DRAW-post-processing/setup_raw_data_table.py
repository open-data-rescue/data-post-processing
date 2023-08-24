import tables
import config


def set_up_raw_data_table(continue_flag):
    tables.add_ppid_column_fields_table()
    tables.update_fields_ppid(1, config.ppid_to_field_id[1])
    tables.update_fields_ppid(2, config.ppid_to_field_id[2])
    tables.update_fields_ppid(3, config.ppid_to_field_id[3])
    tables.update_fields_ppid(4, config.ppid_to_field_id[4])
    tables.update_fields_ppid(5, config.ppid_to_field_id[5])
    tables.update_fields_ppid(6, config.ppid_to_field_id[6])
    tables.update_fields_ppid(7, config.ppid_to_field_id[7])
    # TODO : update other field id's with their respective pp_id

    tables.create_raw_data_table(continue_flag)
