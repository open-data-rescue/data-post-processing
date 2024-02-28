# -*- coding: utf-8 -*-
import database_connection as db
import datetime
import config
import os
import logs as p

cursor = db.cursor

def generateSEFs():
    for sef_type in config.sef_type_to_field_id.keys():
        generateSEF(sef_type)
        
        
def correctValue(value):
    if value == "empty" or value is None:
        return "-999"
    return value

def correctObservationDate(sef_type,observation_date):
    if getPeriod(sef_type)=="24":
        observation_date.minute=0
        observation_date.hour=0
    elif config.sef_apply_utc==True:
        observation_date=observation_date+datetime.timedelta(hours=config.sef_utc_offset)
    return observation_date

def getPeriod(sef_type):
    if config.sef_type_to_start[sef_type]=="mean" or \
        config.sef_type_to_start[sef_type]=="daily" or \
        config.sef_type_to_start[sef_type]=="total":
        return "24"
    else:
        return "0"
    
    
def getFilename(sef_type,type_result_set):
    filename=os.environ.get('DRAW_sef_folder')+os.sep+"McGill_DRAW_1491_"
    
    if len(type_result_set)>0:
        sorted_type_results=sorted(type_result_set)


    # now we can complete the file name
    #we want to remove the leading -999 and the trailing -999
    #Get start
    start_found=0
    index_start=0

    while start_found==0 and index_start<len(type_result_set):
        entry_value=sorted_type_results[index_start].split("\t")[6]
        if entry_value=="-999":
            index_start+=1
        else:
            start_found=1
    #Get end
    end_found=0
    index_end=-1

    while end_found==0 and index_end > -len(type_result_set):
        entry_value=sorted_type_results[index_end].split("\t")[6]
        if entry_value=="-999":

            index_end-=1
        else:
            end_found=1

    if index_start<len(type_result_set):
        startStr=sorted_type_results[index_start].split("\t")
        filename=filename+startStr[0]+"-"+startStr[1]+"_"
        endStr=sorted_type_results[index_end].split("\t")
        filename=filename+endStr[0]+"-"+endStr[1]+"-"+sef_type+".tsv"
        return (filename,index_start,index_end)
    else:
        return (None, None, None)

    
            
    
def generateSEF(sef_type):
    p.log("Generating SEF for type: " + sef_type)
    if type(config.sef_type_to_field_id[sef_type]) == int:
        query="select value,observation_date from data_entries_corrected_final_iso where field_id = {} order by observation_date asc".format(config.sef_type_to_field_id[sef_type])
    else:
        query="select value,observation_date from data_entries_corrected_final_iso where field_id in {} order by observation_date asc".format(config.sef_type_to_field_id[sef_type])
    cursor.execute(query)
    results=cursor.fetchall()
    type_result_set=[]
    for result in results:
        (value, observation_date)=result
        value=correctValue(value)
        observation_date=correctObservationDate(sef_type, observation_date)
        try:
            result_str=str(observation_date.year)+"\t"+str(observation_date.month)+"\t"+str(observation_date.day)+\
                "\t"+str(observation_date.hour)+"\t"+str(observation_date.minute)+"\t"+getPeriod(sef_type)+\
                "\t"+value+"\t|\t\n"
            type_result_set.append(result_str)
        except:
            p.log ("Couldn't generate SEF line for value="+str(value)+", observation date ="+str(observation_date))
        
        
    (filename,index_start,index_end)=getFilename(sef_type, type_result_set)
    if filename is not None: 
        f=open(filename,"w")
        f.write ("SEF\t1.0.0\n")
        f.write ("ID\tID\n")
        f.write ("Name\t1491\n")
        f.write ("Lat\t45.5\n")
        f.write ("Lon\t-73.59\n")
        f.write ("Alt\t49\n")
        f.write ("Source\McGill\n")
        f.write ("Link\thttps://draw.geog.mcgill.ca/\n")
        f.write ("Vbl\t" + config.sef_type_to_unit[sef_type]+"\n")
        f.write ("Stat\t")
        if "mean" in config.sef_type_to_start[sef_type]:
            f.write("mean\n")
        else:
            f.write("point\n")
        f.write ("Unit\t" + config.sef_type_to_unit[sef_type]+"\n")
        f.write("Meta\t")
        f.write("UTCOffset=")
        if (config.sef_apply_utc==True):
            f.write("Applied\tUTCOffset="+str(config.sef_utc_offset))
        else:
            f.write("NO")
        f.write("\n")
        f.write ("Year\tMonth\tDay\tHour\tMinute\tPeriod\tValue\t|\tMeta\n")
        index=0
        sorted_type_results=sorted(type_result_set)
        for res in sorted_type_results:
            if index>=index_start and index<=index_end+len(sorted_type_results):
                f.write(res)
            index+=1

        
        
        
    