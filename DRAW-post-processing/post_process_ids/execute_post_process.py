import database_connection as db
import tables
import observation_reconciliation as reconcile
import remove_low_transcription_users as remove_ltu
import mysql_indexes
import setup_raw_data_table as setup


# Importing post_process_ids.  See config.py for process id to field setting
import post_process_ids.id1.id_1_phase_1 as id1p1
import post_process_ids.id1.id_1_phase_2 as id1p2
import post_process_ids.id1.id_1_phase_3 as id1p3

import post_process_ids.id2.id_2_phase_1 as id2p1
# import post_process_ids.id2.id_2_phase_2 as id2p2
import post_process_ids.id2.id_2_phase_3 as id2p3

import post_process_ids.id3.id_3_phase_1 as id3p1
import post_process_ids.id3.id_3_phase_2 as id3p2
import post_process_ids.id3.id_3_phase_3 as id3p3

import post_process_ids.id4.id_4_phase_1 as id4p1
# import post_process_ids.id4.id_4_phase_2 as id4p2
import post_process_ids.id4.id_4_phase_3 as id4p3

import post_process_ids.id5.id_5_phase_1 as id5p1
# import post_process_ids.id5.id_5_phase_2 as id5p2
import post_process_ids.id5.id_5_phase_3 as id5p3

import post_process_ids.id6.id_6_phase_1 as id6p1
# import post_process_ids.id6.id_6_phase_2 as id6p2
import post_process_ids.id6.id_6_phase_3 as id6p3

import post_process_ids.id7.id_7_phase_1 as id7p1
# import post_process_ids.id7id_7_phase_2 as id7p2
import post_process_ids.id7.id_7_phase_3 as id7p3

import post_process_ids.id8.id_8_phase_1 as id8p1
# import post_process_ids.id8id_8_phase_2 as id8p2
import post_process_ids.id8.id_8_phase_3 as id8p3

import post_process_ids.id9.id_9_phase_1 as id9p1
# import post_process_ids.id9id_9_phase_2 as id9p2
import post_process_ids.id9.id_9_phase_3 as id9p3

import post_process_ids.id10.id_10_phase_1 as id10p1
# import post_process_ids.id10id_10_phase_2 as id10p2
import post_process_ids.id10.id_10_phase_3 as id10p3

import post_process_ids.id11.id_11_phase_1 as id11p1
# import post_process_ids.id10id_10_phase_2 as id10p2
import post_process_ids.id11.id_11_phase_3 as id11p3

import post_process_ids.id12.id_12_phase_1 as id12p1
# import post_process_ids.id12id_12_phase_2 as id12p2
import post_process_ids.id12.id_12_phase_3 as id12p3

import post_process_ids.id13.id_13_phase_1 as id13p1
# import post_process_ids.id13id_13_phase_2 as id13p2
import post_process_ids.id13.id_13_phase_3 as id13p3

#  Check for outliers
import post_process_ids.id1.id_1_outliers as id1outliers
import post_process_ids.id3.id_3_outliers as id3outliers
import phase2_methods as id1p2_methods
import time
import sef_gen

# import argparse


def logPerf(message):
    global tic
    toc = time.perf_counter()
    print(message, end='')
    print(f":  {toc - tic:0.4f} seconds")
    tic = toc


# point data entry to particular post_processing algorithm for phase 1 depending on its post_process_id
def filter_id(pp_id, entry, phase):
    if phase == 1:
        if pp_id == 1:
            id1p1.phase_1(entry)
        if pp_id == 2:
            id2p1.phase_1(entry)
        elif pp_id == 3:
            id3p1.phase_1(entry)
        elif pp_id == 4:
            id4p1.phase_1(entry)
        elif pp_id == 5:
            id5p1.phase_1(entry)
        elif pp_id == 6:
            id6p1.phase_1(entry)
        elif pp_id == 7:
            id7p1.phase_1(entry)
        elif pp_id == 8:
            id8p1.phase_1(entry)
        elif pp_id == 9:
            id9p1.phase_1(entry)
        elif pp_id == 10:
            id10p1.phase_1(entry)
        elif pp_id == 11:
            id11p1.phase_1(entry)
        elif pp_id == 12:
            id12p1.phase_1(entry)
        elif pp_id == 13:
            id13p1.phase_1(entry)
        else:
            tables.add_to_corrected_table(*entry, 0)
    if phase == 2:
        if pp_id == 1:
            if entry[0] in pressure_lead_digs_added:
                id1p2.phase_2(entry, True)
            else:
                id1p2.phase_2(entry, False)
        elif pp_id == 3:
            pass
        else:
            tables.add_to_final_corrected_table(*entry)
    if phase == 3:
        if pp_id == 1:
            id1p3.phase_3(entry)
        elif pp_id == 2:
            id2p3.phase_3(entry)
        elif pp_id == 3:
            id3p3.phase_3(entry)
        elif pp_id == 4:
            id4p3.phase_3(entry)
        elif pp_id == 5:
            id5p3.phase_3(entry)
        elif pp_id == 6:
            id6p3.phase_3(entry)
        elif pp_id == 7:
            id7p3.phase_3(entry)
        elif pp_id == 8:
            id8p3.phase_3(entry)
        elif pp_id == 9:
            id9p3.phase_3(entry)
        elif pp_id == 10:
            id10p3.phase_3(entry)
        elif pp_id == 11:
            id11p3.phase_3(entry)
        elif pp_id == 12:
            id12p3.phase_3(entry)
        elif pp_id == 13:
            id13p3.phase_3(entry)

    elif phase == 'outlier_removal':
        if pp_id == 1:
            return id1outliers.patch_outlier(entry)
            pass
        elif pp_id == 3:
            return id3outliers.patch_outlier(entry)
            return
        else:
            pass


tic = time.perf_counter()

# Experimental: implement a continue flag
continue_flag = True
# parser = argparse.ArgumentParser()
# parser.add_argument("-c", help="Continues - do not process data already processed", action="store_true")
# args = parser.parse_args()
# if args.c:
#     continue_flag=True


#           TAKE IN RAW DATA AND CREATE "raw_data_entries" TABLE       #########################
setup.set_up_raw_data_table(continue_flag)
mysql_indexes.data_entries_raw('user', 'create')

logPerf("Created raw data entries")

#           REMOVE ENTRIES WITH NO OBSERVATION DATE      ######################
remove_ltu.delete_transcriptions()
mysql_indexes.data_entries_raw('user', 'delete')

logPerf("Removed entries from users with less than 100 records")

#          REMOVE ENTRIES FROM USERS WITH LESS THAN 100 TOTAL TRANSCRIBED ENTRIES       #############
remove_ltu.delete_transcriptions()
mysql_indexes.data_entries_raw('user', 'delete')

logPerf("Removed entries from users with less than 100 records")


#               EXECUTE PHASE 1 (FORMAT CHECKING/CLEANING)       ###############################
mysql_indexes.data_entries_raw('annotation', 'create')
mysql_indexes.data_entries_raw('observation', 'create')
mysql_indexes.data_entries_raw('field_date', 'create')
raw_entries = db.raw_data()


tables.create_corrected_data_table()
tables.create_error_edit_table(1, continue_flag)

logPerf("Created indexed for raw data processing")

print("Phase 1: ")
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
logPerf("Phase 1 complete")

# Save corrected data in database
tables.populate_corrected_table()
tables.populate_error_edit_code(1)

#               RECONCILE VALUES FOR SAME OBSERVATION (FIELD + DATETIME)       ###################
mysql_indexes.data_entries_corrected('field_date_user', 'create')
tables.create_duplicateless_table()
reconcile.remove_duplicates()

logPerf("Removed duplicates")
mysql_indexes.data_entries_corrected_duplicateless('field_date', 'create')


#               EXECUTE PHASE 2 (REMOVE OUTLIERS + STATISTICAL/VALIDATION CHECKING)       ###################
tables.create_final_corrected_table(continue_flag)
tables.create_error_edit_table(2, continue_flag)
entries = db.phase_1_data()

for index in range(len(entries)):
    row_list = list(entries[index])
    post_process_id = row_list[8]
    outlier_fixed = filter_id(post_process_id, row_list, 'outlier_removal')
    if outlier_fixed is not None:
        row_list[1] = outlier_fixed
    row = tuple(row_list)
    entries[index] = row

logPerf("Removed outliers")

pressure_lead_digs_added = id1p2_methods.pressure_artificial_lead_digs_list()
counter = 0
print("Phase 2:")
for row in entries:
    post_process_id = row[8]
    filter_id(post_process_id, row, 2)
    counter += 1
    if (counter % 1000) == 0:
        print('.', end="")
    if (counter % 50000) == 0:
        print("")

logPerf("Completed post-process 1 phase 2")
id3p2.phase_2(entries)
logPerf("Completed post-process 3 phase 2")

tables.populate_final_corrected_table()
tables.populate_error_edit_code(2)

logPerf("Phase 2 complete")

#                 EXECUTE PHASE 3 (ISO TRANSLATION)       #########################
print("Phase 3:")
tables.create_final_corrected_table_iso(continue_flag)
entries = db.phase_2_data()
for row in entries:
    post_process_id = row[8]
    filter_id(post_process_id, row, 3)
    counter += 1
    if (counter % 1000) == 0:
        print('.', end="")
    if (counter % 50000) == 0:
        print("")
tables.populate_final_corrected_table_iso()

logPerf("Completed phase 3")


#               DELETE ALL DISPENSABLE TABLES (KEEP FINAL + ERRORS/EDITS TABLES)       ##########
tables.delete_table('data_entries_raw')
tables.delete_table('data_entries_corrected')
tables.delete_table('data_entries_corrected_duplicateless')
logPerf("cleaned up database")


#           Generating SEF files ##########################
print("Generating SEF files")
sef_gen.generateSEFs()
logPerf("SEF files generated")
