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
    tables.update_fields_ppid(8, config.ppid_to_field_id[8])
    tables.update_fields_ppid(9, config.ppid_to_field_id[9])
    tables.update_fields_ppid(10, config.ppid_to_field_id[10])
    tables.update_fields_ppid(11, config.ppid_to_field_id[11])
    tables.update_fields_ppid(12, config.ppid_to_field_id[12])
    tables.update_fields_ppid(13, config.ppid_to_field_id[13])
    # TODO : update other field id's with their respective pp_id

    tables.create_raw_data_table(continue_flag)
