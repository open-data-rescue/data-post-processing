import post_process_ids.id3.id_3_phase_2 as id3p2
import database_connection as db
import time

tic=time.perf_counter()
data_entries=db.phase_1_data_test()
id3p2.phase_2(data_entries)
toc=time.perf_counter()
print(f"Done in:  {toc - tic:0.4f} seconds")
