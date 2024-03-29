# file used to store commands for creating, editing and managing MySQL tables throughout post-processing workflow

import mysql.connector.errors
import database_connection as db
import sql_commands as sql
import pandas as pd
import config

db_conn = db.conn
cursor = db.cursor
corrected_table=db.corrected_table
final_corrected_table=db.final_corrected_table
final_corrected_table_iso=db.final_corrected_table_iso
phase_1_errors=db.phase_1_errors
phase_2_errors=db.phase_2_errors
duplicateless=db.duplicateless

# adds 'post_process_id' column to fields table, necessary before creating raw data table for post-processing
def add_ppid_column_fields_table():
    try:
        add_ppid_column = "ALTER TABLE fields ADD COLUMN post_process_id INT;"
        cursor.execute(add_ppid_column)
    except mysql.connector.errors.ProgrammingError:
        pass


# update fields table in DRAW database with relevant post_process_id's (e.g. '1' for pressure values)
def update_fields_ppid(post_process_id, field_id_tuple):
    if type(field_id_tuple) != tuple:
        field_id_tuple = '({})'.format(field_id_tuple)
    add_post_process_ids = "UPDATE fields " \
                           "SET post_process_id = {} " \
                           "WHERE id IN {};".format(post_process_id, field_id_tuple)
    cursor.execute(add_post_process_ids)
    db_conn.commit()


# command to create composite raw data table from data entries, fields and annotations tables; creating this table is necessary as it enables the
# addition of indexes (which speeds up code considerably during runtime) and standardizes organization of data in DRAW post-processing
def create_raw_data_table(continue_flag):
    cursor.execute("DROP TABLE IF EXISTS data_entries_raw;")
    if continue_flag == True:
        cursor.execute(sql.composite_raw_data_entries_continue)
    else:
        cursor.execute(sql.composite_raw_data_entries)

# create 'data_entries_corrected' table to store values after cleaned in phase 1
def create_corrected_data_table():
    cursor.execute("DROP TABLE IF EXISTS data_entries_corrected;")
    create_table = "CREATE TABLE data_entries_corrected AS SELECT * FROM data_entries_raw LIMIT 0;"
    cursor.execute(create_table)
    add_flagged_column = "ALTER TABLE data_entries_corrected ADD flagged INT NOT NULL;"
    cursor.execute(add_flagged_column)
    db_conn.commit()


# create 'data_entries_corrected_duplicateless' table to store values after reconciled (post-phase 1)
def create_duplicateless_table():
    cursor.execute("DROP TABLE IF EXISTS data_entries_corrected_duplicateless;")
    cursor.execute("CREATE TABLE IF NOT EXISTS data_entries_corrected_duplicateless AS SELECT * FROM data_entries_corrected LIMIT 0;")
    cursor.execute("SELECT COUNT(*) FROM data_entries_corrected_duplicateless;")
    count = cursor.fetchall()[0][0]
    if count != 0:
        cursor.execute("DELETE FROM data_entries_corrected_duplicateless;")
        db_conn.commit()


# creates 'data_entries_corrected_final' table for post-phase 2 processed data
def create_final_corrected_table(continue_flag):
    if continue_flag is False:
        cursor.execute("DROP TABLE IF EXISTS data_entries_corrected_final;")
        create_table = "CREATE TABLE data_entries_corrected_final AS SELECT * FROM data_entries_corrected_duplicateless LIMIT 0;"
        cursor.execute(create_table)

# creates 'data_entries_corrected_final_iso' table for post-phase 2 processed data iso transformation
def create_final_corrected_table_iso(continue_flag):
    if continue_flag is False:
        cursor.execute("TRUNCATE TABLE data_entries_corrected_final_iso;")
        create_table = "CREATE TABLE data_entries_corrected_final_iso AS SELECT * FROM data_entries_corrected_final LIMIT 0;"
        cursor.execute(create_table)

# creates 'data_entries_phase_{}_errors' table for error and edit documentation
def create_error_edit_table(phase,continue_flag):
    if continue_flag is False:
        cursor.execute("DROP TABLE IF EXISTS data_entries_phase_{}_errors;".format(phase))
        cursor.execute(sql.create_error_edit_table(phase))


# adds entry to "data_entries_corrected" table
def add_to_corrected_table(entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged):
    global corrected_table
    corrected_table.append([entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged])
    if len(corrected_table)>50000:
        populate_corrected_table()
        corrected_table=[]

def populate_corrected_table():
    sql_command = "INSERT INTO data_entries_corrected " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.executemany(sql_command, corrected_table)
    db_conn.commit()

# adds entry to "data_entries_corrected" table
def add_to_final_corrected_table_iso(entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged):
    global final_corrected_table_iso
    final_corrected_table_iso.append([entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged])
    if len(final_corrected_table_iso)>50000:
        populate_final_corrected_table_iso()
        final_corrected_table_iso=[]

def populate_final_corrected_table_iso():
    sql_command = "INSERT INTO data_entries_corrected_final_iso " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.executemany(sql_command, final_corrected_table_iso)
    db_conn.commit()

# adds entry to "data_entries_corrected_final" table (after phase 2 checking)
def add_to_final_corrected_table(entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged):
    global final_corrected_table
    final_corrected_table.append([entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged])
    if len(final_corrected_table)>50000:
        populate_final_corrected_table()
        final_corrected_table=[]

def populate_final_corrected_table():
    sql_command = "INSERT INTO data_entries_corrected_final " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.executemany(sql_command, final_corrected_table)
    db_conn.commit()



# add flag or edit made to particular value to "data_entries_phase_{}_errors" table (depending on chosen input parameter, can be for phase 1 or 2)
def add_error_edit_code(phase, error_code, original_value, corrected_value, entry_list, add_info=''):
    entry_id = entry_list[0]
    user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date = [None for i in range(8)]
    if phase == 1:
        user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date = entry_list[2:]  # deal with 10 rows
        phase_1_errors.append([entry_id, original_value, corrected_value, error_code, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, add_info])
    elif phase == 2:
        user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date = entry_list[2:len(entry_list) - 1]  # deal with 11 rows
        phase_2_errors.append([entry_id, original_value, corrected_value, error_code, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, add_info])


def populate_error_edit_code(phase):
    sql_command = "INSERT INTO data_entries_phase_{}_errors " \
                  "(id, ORIGINAL_VALUE, CORRECTED_VALUE, error_code, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, additional_info) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);".format(phase)

    if phase==1:
        cursor.executemany(sql_command, phase_1_errors)
    elif phase==2:
       # cursor.executemany(sql_command, phase_2_errors)
        #create data frame from phase 2 errors, instead of above
        #data frame.to_sql
        df_temp=pd.DataFrame(phase_2_errors,
                        columns=[ 'id', 'ORIGINAL_VALUE', 'CORRECTED_VALUE', 'error_code', 'user_id', 'page_id', 'field_id', 'field_key', 'annotation_id', 'transcription_id', 'post_process_id', 'observation_date', 'additional_info'])
        df_temp.to_sql('data_entries_phase_2', db.engine, if_exists='append', index=False)
    db_conn.commit()




# add reconciled observation entry to duplicateless table (after phase 1)
def add_to_duplicateless_table(entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged):
    global duplicateless
    duplicateless.append([entry_id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged])
    if len(duplicateless)>50000:
        populate_duplicateless_table()
        duplicateless=[]

def populate_duplicateless_table():
    sql_command = "INSERT INTO data_entries_corrected_duplicateless " \
                  "(id, value, user_id, page_id, field_id, field_key, annotation_id, transcription_id, post_process_id, observation_date, flagged) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.executemany(sql_command, duplicateless)
    db_conn.commit()

# updates duplicateless table - used to update MySQL table during observation reconciliation, before continuing with phase 2
def update_duplicateless_table(value, entry_id):
    sql_command = "UPDATE data_entries_corrected_duplicateless " \
                  "SET value = %s " \
                  "WHERE id = %s;"
    cursor.execute(sql_command, (value, entry_id))
    db_conn.commit()

# get annotations that have been inserted in error edit code table for a given ppid
def get_error_code_annotations(phase, ppid):
    sql_command= "select annotation_id from data_entries_phase_{}_errors ".format(phase)
    sql_command=sql_command + "where post_process_id='"+ppid+"'"
    cursor.execute(sql_command)
    return cursor.fetchall()


# deletes MySQL table at the very end of post-processing
def delete_table(name):
    sql_command = "DROP TABLE {};".format(name)
    cursor.execute(sql_command)

# Create PostProcessing table
def create_post_processing_reports_table():
    sql_command="CREATE TABLE IF NOT EXISTS post_processing_reports ( "\
        "id int NOT NULL auto_increment,"\
        "runtime datetime NOT NULL, "\
        "report MEDIUMTEXT NOT NULL,"\
        "PRIMARY KEY (id))"
    cursor.execute(sql_command)
    db_conn.commit()
    
def create_outliers_stats_table():
    sql_command="CREATE TABLE IF NOT EXISTS outlier_stats ( "\
        "id int NOT NULL auto_increment,"\
        "report_id int NOT NULL, "\
        "field_id varchar(32) default '',"\
        "count int not null default 0,"\
        "PRIMARY KEY (id))"
    cursor.execute(sql_command)
    db_conn.commit()

def writeReport (report_out, start_time):
    sql_command="INSERT INTO post_processing_reports (runtime, report) values (%s,%s)"
    cursor.execute(sql_command, (start_time, report_out))
    db_conn.commit()
    return cursor.lastrowid

def create_outliers_graphs():
    sql_command="CREATE table if not exists outlier_graphs ("\
        "id int not null auto_increment,"\
        "report_id int not null,"\
        "field_id  int not null,"\
        "data  text not null, "\
        "primary key (id))"
    cursor.execute(sql_command)
    db_conn.commit()
    
def insert_outlier_graphs(report_id,graphs):
    for graph in graphs:
        if len(graph) >0:
            (field_id,data)=graph[0]
            sql_command="insert into outlier_graphs "\
                "(report_id,field_id,data) "\
                "values (%s, %s, %s);"
            cursor.execute(sql_command,(report_id,field_id,data))
            db_conn.commit()
        
def insert_outlier_stats(report_id,stats):
    for stat in stats:
        (field_id,count)=stat
        sql_command="insert into outlier_stats "\
            "(report_id,field_id,count) "\
            "values (%s, %s, %s);"
        cursor.execute(sql_command, (report_id,field_id,count))
        db_conn.commit()