import mysql.connector
import sql_commands
import os

corrected_table=[]
final_corrected_table=[]
phase_1_errors=[]
phase_2_errors=[]
duplicateless=[]

# connection to copy of database on local machine
conn = mysql.connector.connect(
    #####   FOLLOWING 3 VARIABLES TO BE CONFIGURED AS NECESSARY FOR LOCAL MACHINE:   #####
    user=os.environ.get('DRAW_local_db_user'),
    password=os.environ.get('DRAW_local_db_pass'),
    #user='vicky',
    #password='password',
    database='climate_test',
    #database='climatedatarescue',
    host='localhost'
)

cursor = conn.cursor()


# returning raw data entries from database, with all necessary information (columns)
def raw_data():
    sql_command = sql_commands.raw_data_sql
    cursor.execute(sql_command)
    result = cursor.fetchall()
    return result


# returning phase 1-corrected, duplicateless data entries => for phase 2
def phase_1_data():
    sql_command = sql_commands.phase_1_data_sql
    cursor.execute(sql_command)
    result = cursor.fetchall()
    return result
