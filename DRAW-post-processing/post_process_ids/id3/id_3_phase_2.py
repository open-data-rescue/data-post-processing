
import pandas as pd
import tables
import database_connection as db
import config
import math
import time
#import numpy as np
# curve-fit() function imported from scipy
#from scipy.optimize import curve_fit
from matplotlib import pyplot as plt


def log_errors(code,errors):
    for error in errors.iterrows():
        tables.add_error_edit_code(2, code, error[1].value, '-999',error[1])

# compares observed and corrected values. If not within a threshold, they are both marked as error [304]
def compare_observed_corrected (df,field_observed,field_corrected):
    print("   Comparing observed vs corrected for fields " + str(field_observed)+" vs "+str(field_corrected))
    df_comp=df[df['field_id'].isin([field_observed,field_corrected]) ]
    temp_observed_errors=df_comp.groupby(['observation_date'])['value'].diff().dropna().abs().gt(config.temperature_difference_allowed_obs_corr)

    errors_date_temp=df_comp[df_comp.observation_date.isin(
       df_comp[df_comp.index.isin
               (temp_observed_errors[temp_observed_errors].index.values)
               ].observation_date)] 
    log_errors('302', errors_date_temp)    


# verifies that min is less than max at a given time. If not, both entries are marked as errors [305]
def compare_min_max (df,field_min,field_max):
    print("   Comparing min/max for fields "+str(field_min) +"/"+str(field_max))
    df_comp=df[df['field_id'].isin([field_min,field_max])].sort_values(by=['observation_date'])
    obs_date=None
    min_temp=math.nan
    max_temp=math.nan
    for index, row in df_comp.iterrows():
        if obs_date == None or obs_date != row['observation_date'] :
            #new day, resetting everything            
            obs_date=row['observation_date']
            min_temp=math.nan
            max_temp=math.nan
        
        if row['field_id'] == field_min:
            min_temp=row['value']
        elif row['field_id'] == field_max:
            max_temp=row['value']
        if not (math.isnan(min_temp)) and not math.isnan(max_temp) and min_temp>max_temp:
            entries_date=df_comp[df_comp.observation_date==obs_date]
            log_errors('305', entries_date)

# Verifies that the first field in the list is less than all other fields - same observation time. If not, marked as flagged [2]
def compare_field_less_than_other_fields(df,fields):
    print ("   Comparing that field "+str(fields[0])+" is less than these fields: "+str(fields[1])) 
    df_comp=df[df['field_id'].isin(fields)].sort_values(by=['observation_date'])
    obs_date=None
    min_temp=math.nan
    max_temp=math.nan
    min_index=math.nan
    max_index=math.nan
    for index, row in df_comp.iterrows():
        if obs_date == None or obs_date != row['observation_date'] :
            if not (math.isnan(min_temp)) and not math.isnan(max_temp) and min_temp>max_temp:
               df.at[min_index,'flagged']=2 
               df.at[max_index,'flagged']=2
               
            # new day, resetting everything            
            obs_date=row['observation_date']
            min_temp=math.nan
            max_temp=math.nan
        if row['field_id'] == fields[0]:  
            min_temp=row['value']
            min_index=index
        else:
            #determine max_temp as the minimum of the values of the fields that are not the first field (fields[0])
            if math.isnan(max_temp):
                max_temp=row['value']
                max_index=index
            else: 
                if row.value <max_temp:
                    max_temp=row.value
                    max_index=index

# check the the min field is the min of all previous fields between last min field measurement or 24 hours. If not marked as flagged [3]
def check_field_is_min_over_period(df,min_field,max_field):
    print ("   Checking that field "+str(min_field)+" is the minimum of all values of this field: "+str(max_field))       
    df_comp=df[df['field_id'].isin([min_field,max_field])].sort_values(by=['observation_date'])
    obs_date=None
    min_temp=math.nan
    max_data=[]
    for index, row in df_comp.iterrows():
        if row.field_id==min_field:
            obs_date=row.observation_date
            min_temp=row.value
            #check if the max_temp value lower
            for data in max_data:
                delta_time=obs_date-data[2]
                if delta_time.days<1: #ensuring that we are comparing values at most 1 day earlier
                    if data[1]<min_temp:
                        df.at[data[0],'flagged']=3
                        df.at[index,'flagged']=3
            max_data=[]
        else:
            max_data.append([index,row.value,row.observation_date])
                
# check that the max field is the max of all previous fields between last max field measurement or 24 hours. If not marked as flagged [4]                
def check_field_is_max_over_period(df,max_field,min_field):
    print ("   Checking that field "+str(max_field)+" is the maximum of all values of this field: "+str(min_field))       
    df_comp=df[df['field_id'].isin([max_field,min_field])].sort_values(by=['observation_date'])
    obs_date=None
    max_temp=math.nan
    min_data=[]
    for index, row in df_comp.iterrows():
        if row.field_id==max_field:
            obs_date=row.observation_date
            max_temp=row.value
            #check if the max_temp value lower
            for data in min_data:
                delta_time=obs_date-data[2]
                if delta_time.days<1: #ensuring that we are comparing values at most 1 day earlier
                    if data[1]>max_temp:
                        df.at[data[0],'flagged']=4
                        df.at[index,'flagged']=4
            min_data=[]
        else:
            min_data.append([index,row.value,row.observation_date])
    

   

def compare_min_max_df (df,field_min,field_max):
    #Keeping the code, but 4 times slower than compare_min_max
    df_comp=df[df['field_id'].isin([field_min,field_max])].sort_values(by=['observation_date'])
    temp_entries=df_comp.groupby(['observation_date'])['value','field_id']
    for observation_date, data in temp_entries:
        if data.shape[0]>1:
            min_temp=data[data.field_id==field_min].iloc[0][0]
            max_temp=data[data.field_id==field_max].iloc[0][0]
            if not (math.isnan(min_temp)) and not math.isnan(max_temp) and min_temp>max_temp:
                entries_date=df_comp[df_comp.observation_date==observation_date]
                log_errors('303', entries_date)

# checks air temperature and wet bulb are less than a certain threshold
def check_air_wet_bulb(df, fields):
    print ("   Checking wet bulb for fields: "+str(fields))       
    df_comp=df[df['field_id'].isin([fields])].sort_values(by=['observation_date'])
    obs_date=None
    f0=math.nan
    f1=math.nan
    f2=math.nan
    f0_index=math.nan
    f1_index=math.nan
    f2_index=math.nan
    for index, row in df_comp.iterrows():
        if obs_date!=None and row.observation_date != obs_date:
            #new date, so check if we got field values
            if math.isnan(f0)==False and math.isnan(f1)==False and math.isnan(f2)==False \
                and abs(abs(f0-f1)-abs(f2)) > config.temperature_air_wet_bulb_threshold:
                    df.at[f0_index,'flagged']=5
                    df.at[f1_index,'flagged']=5
                    df.at[f2_index,'flagged']=5
            f0=math.nan
            f1=math.nan
            f2=math.nan
            f0_index=math.nan
            f1_index=math.nan
            f2_index=math.nan   
        if row.field_id==fields[0]:
            f0=row.value
            f0_index=index
        elif row.field_id==fields[1]:
            f1=row.value
            f1_index=index
        elif row.field_id==fields[2]:
            f2=row.value
            f2_index=index

   
    
# Detects outliers and flags them [1]
def flag_outliers (df, field_id):


    df_proc=df[df.field_id==field_id].sort_values(by=['observation_date'])
    
    #determine list of series that are eligible for validation based on rule: needs less than 5 days before or after with no data
    obs_date=None
    list_partial=[]
    for index,row in df_proc.iterrows():
        if (obs_date==None or (row['observation_date']-obs_date).days<5) and len(list_partial)<100:
            list_partial.append(row)
            obs_date=row['observation_date']
        else:
            df_partial=pd.DataFrame(list_partial)
            
            x=df_partial.observation_date
            y=df_partial.value
            if y.size>6:
                #param, param_cov = curve_fit(test,x,y)
                ans=y.rolling(5, center=True).mean()   
                delta=(y-ans).abs()
                standard_deviation=delta.std()
                outliers=df_proc[df_proc.index.isin(delta[delta.gt(config.temperature_outlier_std_factor*standard_deviation)].index)]
                if outliers.size >0:
                    if config.temperature_plot_outliers == True:
                        ans_max=ans+config.temperature_outlier_std_factor*standard_deviation
                        ans_min=ans-config.temperature_outlier_std_factor*standard_deviation   
                        fig, ax = plt.subplots(1, figsize = (20, 8))
                        fig.autofmt_xdate()
                        ax.plot(x, y, '.', color ='black', label ="data")
                        ax.plot(x, ans, '--', color ='blue', label ="rolling mean")
                        ax.plot(x,ans_max,'-.', color='green', label=str(config.temperature_outlier_std_factor)+" sigma")
                        ax.plot(x,ans_min,'-.', color='green')
                        ax.plot(outliers.observation_date, outliers.value,'o', color='red', label="Outliers")
                        ax.set_title("Field: " +str(field_id)+" - " + df_partial.field_key.iloc[0])
                        ax.legend()
                        #plt.ion()
                        #ax.show()
                    #flag the outliers
                    for ind,outlier in outliers.iterrows():
                        df.at[ind,'flagged']=10
                        
            obs_date=row['observation_date']
            list_partial=[]
            list_partial.append(row)





def phase_2(entries,debug=False):
    
    def logPerf(tic,message):
        toc = time.perf_counter()
        print(message, end='')
        print (f":  {toc - tic:0.4f} seconds")
        return toc
    
    print ("Starting temperature phase 2")
    tic = time.perf_counter()
    # execute post process id3 on the whole dataset, not one entry at a time
    df=pd.DataFrame(entries, 
                    columns=['id','value','user_id','page_id','field_id','field_key',
                             'annotation_id','transcription_id','post_process_id',
                             'observation_date','flagged'])
    
    # Filtering to get only data entries for post process ID 3 that are not empty or retracted, then transform value to numeric
    df_temp=df[df.post_process_id==3]
    pd.options.mode.chained_assignment = None
    df_temp['value']=pd.to_numeric(df_temp['value'],errors='coerce')
    df_temp_nona=df_temp.dropna()
    tic=logPerf(tic, "Filtered numeric data for temperature")
    
    # processing difference between temp corrected and observed
    for field in config.temperature_corr_observed_fields:
        compare_observed_corrected(df_temp_nona, field[0], field[1])
    tic=logPerf(tic, "Completed observed vs corrected checks")
   
    # check max temp of a day is always > min temp of day
    for field in config.temperature_min_max_fields:
        compare_min_max(df_temp_nona, field[0], field[1])
    tic=logPerf(tic, "Completed min vs max checks")
 
    # check temperature is less than other fields
    for fields in config.temperature_less_than_other_fields:
        compare_field_less_than_other_fields(df_temp_nona,fields)
    tic=logPerf(tic, "Completed field less than other fields")
    
    # check temperature is the min of other values within past 24 hours max
    for fields in config.temperature_min_fields:
        check_field_is_min_over_period(df_temp_nona, fields[0], fields[1])
    tic=logPerf(tic, "Completed field is minimum of other fields over period of time")
    
    # check temperature is the max of other values within past 24 hours max
    for fields in config.temperature_max_fields:
        check_field_is_max_over_period(df_temp_nona, fields[0], fields[1])
    tic=logPerf(tic, "Completed field is maximum of other fields over period of time")   

    # check wet bulb
    for fields in config.temperature_air_wet_bulb:
        check_air_wet_bulb(df_temp_nona, fields)
    tic=logPerf(tic, "Completed field is maximum of other fields over period of time")   
        
    # statistical outliers
    if debug==False: 
        tables.populate_error_edit_code(2)
        # get list of annotation ids from error table and remove them from df_temp_nona
        annotations=tables.get_error_code_annotations('2','3')
        df_temp_cleaned=df_temp_nona[~df_temp_nona.annotation_id.isin(annotations)]
    else:
        df_temp_cleaned=df_temp_nona
    tic=logPerf(tic, "Completed removing detected errors before outlier detection")
    
    # get series of values for a given field ID
    for field in config.temperature_stat_outliers:
        flag_outliers(df_temp_cleaned, field)
    tic=logPerf(tic, "Completed outlier detection")


    # fit the series
    df_temp_cleaned.to_sql('data_entries_corrected_final', db.engine, if_exists='append', index=False)

    