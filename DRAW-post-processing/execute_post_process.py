import database_connection as db
import tables
import observation_reconciliation as reconcile
import remove_low_transcription_users as remove_ltu
import mysql_indexes
import setup_raw_data_table as setup
#import numpy as np
#import pandas as pd

# Importing post_process_id = 1:
import post_process_ids.id1.id_1_phase_1 as id1p1
import post_process_ids.id1.id_1_phase_2 as id1p2
import post_process_ids.id1.id_1_outliers as id1outliers
import id1p2_methods
import time
import argparse



# point data entry to particular post_processing algorithm for phase 1 depending on its post_process_id
def filter_id(pp_id, entry, phase):
    if phase==1:
        if pp_id==1:
            id1p1.phase_1(entry)
        else:
            tables.add_to_corrected_table(*entry, 0)
    elif phase==2:
        if pp_id==1:
            if entry[0] in pressure_lead_digs_added:
                id1p2.phase_2(entry, True)
            else:
                id1p2.phase_2(entry, False)
        else:
            tables.add_to_final_corrected_table(*entry)
 
    elif phase== 'outlier_removal':
        if pp_id ==1:
            return id1outliers.patch_outlier(entry)
        else:
            pass

tic = time.perf_counter()
continue_flag=False

parser = argparse.ArgumentParser()
parser.add_argument("-c", help="Continues - do not process data already processed", action="store_true")
args = parser.parse_args()
if args.c:
    continue_flag=True


#####################       TAKE IN RAW DATA AND CREATE "raw_data_entries" TABLE       ########################################
setup.set_up_raw_data_table(continue_flag)
mysql_indexes.data_entries_raw('user', 'create')

toc=time.perf_counter()
print(f"Created raw data entries:  {toc - tic:0.4f} seconds")
tic=toc

#####################       REMOVE ENTRIES FROM USERS WITH LESS THAN 100 TOTAL TRANSCRIBED ENTRIES       ######################
remove_ltu.delete_transcriptions()
mysql_indexes.data_entries_raw('user', 'delete')
toc=time.perf_counter()
print(f"Removed entries from users with less than 100 records:  {toc - tic:0.4f} seconds")
tic=toc

#####################       EXECUTE PHASE 1 (FORMAT CHECKING/CLEANING)       ##################################################
mysql_indexes.data_entries_raw('annotation', 'create')
mysql_indexes.data_entries_raw('observation', 'create')
mysql_indexes.data_entries_raw('field_date', 'create')
raw_entries = db.raw_data()
tables.create_corrected_data_table()
tables.create_error_edit_table(1,continue_flag)
toc=time.perf_counter()
print(f"Created indexed for raw data processing:  {toc - tic:0.4f} seconds")
tic=toc
print ("Phase 1: ")
counter = 0
for row in raw_entries:
    post_process_id = row[8]
    filter_id(post_process_id, row, 1)
    counter += 1
    if (counter % 1000) == 0:
        print('.', end="")
    if (counter % 50000) == 0:
        print("")
print("")
toc=time.perf_counter()
print (f"Phase 1 complete: {toc - tic:0.4f} seconds")
tic=toc
# Save corrected data in database
tables.populate_corrected_table()
tables.populate_error_edit_code(1)

#####################       RECONCILE VALUES FOR SAME OBSERVATION (FIELD + DATETIME)       ####################################
mysql_indexes.data_entries_corrected('field_date_user', 'create')
tables.create_duplicateless_table()
reconcile.remove_duplicates()
toc=time.perf_counter()
print (f"Removed duplicates: {toc - tic:0.4f} seconds")
tic=toc
mysql_indexes.data_entries_corrected_duplicateless('field_date', 'create')


#####################       EXECUTE PHASE 2 (REMOVE OUTLIERS + STATISTICAL/VALIDATION CHECKING)       #########################
entries = db.phase_1_data()
tables.create_final_corrected_table(continue_flag)
tables.create_error_edit_table(2,continue_flag)

for index in range(len(entries)):
    row_list = list(entries[index])
    post_process_id = row_list[8]
    outlier_fixed = filter_id(post_process_id, row_list, 'outlier_removal')
    if outlier_fixed is not None:
        row_list[1] = outlier_fixed
    row = tuple(row_list)
    entries[index] = row
    
toc=time.perf_counter()
print (f"Removed outliers: {toc - tic:0.4f} seconds")
tic=toc

pressure_lead_digs_added = id1p2_methods.pressure_artificial_lead_digs_list()

counter = 0
print ("Phase 2:")
for row in entries:
    post_process_id = row[8]
    filter_id(post_process_id, row, 2)
    counter += 1
    if (counter % 1000) == 0:
        print('.', end="")
    if (counter % 50000) == 0:
        print("")

tables.populate_final_corrected_table()
tables.populate_error_edit_code(2)    
toc=time.perf_counter()
print (f"Phase 2 complete: {toc - tic:0.4f} seconds")
tic=toc

#####################       DELETE ALL DISPENSABLE TABLES (KEEP FINAL + ERRORS/EDITS TABLES)       ############################
tables.delete_table('data_entries_raw')
tables.delete_table('data_entries_corrected')
tables.delete_table('data_entries_corrected_duplicateless')
