import post_process_ids.id3.id_3_phase_2 as id3p2
import database_connection as db
import time
#import tables

tic=time.perf_counter()
print("Creating error_table")
#tables.create_error_edit_table(2,False)
print("Created error edit phase 2 table")

data_entries=db.phase_1_data_test()
print("Loaded phase 1 output test data")
id3p2.phase_2(data_entries,debug=True)
toc=time.perf_counter()
print(f"Done in:  {toc - tic:0.4f} seconds")
