import mysql.connector
import sql_commands
import sqlalchemy
import os

corrected_table=[]
final_corrected_table=[]
final_corrected_table_iso=[]
phase_1_errors=[]
phase_2_errors=[]
duplicateless=[]

db_user=os.environ.get('DRAW_local_db_user')
db_passwd=os.environ.get('DRAW_local_db_pass')
db_name=os.environ.get('DRAW_local_db_name')
db_host=os.environ.get('DRAW_db_host')

# connection to copy of database on local machine
conn = mysql.connector.connect(
    #####   FOLLOWING 3 VARIABLES TO BE CONFIGURED AS NECESSARY FOR LOCAL MACHINE:   #####
    user=db_user,
    password=db_passwd,
    database=db_name,
    host=db_host
)

cursor = conn.cursor()

url = "mysql+mysqlconnector://"+db_user+":"+db_passwd+"@"+db_host+"/"+db_name
engine = sqlalchemy.create_engine(url)


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

def phase_1_data_test():
    sql_command = sql_commands.phase_1_data_test_sql
    cursor.execute(sql_command)
    result = cursor.fetchall()
    return result

def phase_2_data():
    sql_command = sql_commands.phase_2_data_sql
    cursor.execute(sql_command)
    result = cursor.fetchall()
    return result

def outliers_stats():
    sql_command=sql_commands.outliers_stats_sql
    cursor.execute(sql_command)
    result = cursor.fetchall()
    return result    