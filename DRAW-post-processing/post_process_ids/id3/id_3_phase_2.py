
import pandas as pd
import tables
import config
import math

def log_errors(code,errors):
    for error in errors.iterrows():
        tables.add_error_edit_code(2, code, error[1].value, '-999',error[1])


def compare_observed_corrected (df,field_observed,field_corrected):
    df_comp=df[df['field_id'].isin([field_observed,field_corrected]) ]
    temp_observed_errors=df_comp.groupby(['observation_date'])['value'].diff().dropna().abs().gt(config.temperature_difference_allowed_obs_corr)

    errors_date_temp=df_comp[df_comp.observation_date.isin(
       df_comp[df_comp.index.isin
               (temp_observed_errors[temp_observed_errors].index.values)
               ].observation_date)] 
    log_errors('304', errors_date_temp)    



def compare_min_max (df,field_min,field_max):
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
                log_errors('305', entries_date)
   
def flag_outliers (df, field_id):
    df_proc=df[df.field_id==field_id]

def phase_2(entries):
    # execute post process id3 on the whole dataset, not one entry at a time
    df=pd.DataFrame(entries, 
                    columns=['id','value','user_id','page_id','field_id','field_key',
                             'annotation_id','transcription_id','post_process_id',
                             'observation_date','flagged'])
    
    # Filtering to get only data entries for post process ID 3 that are not empty or retracted, then transform value to numeric
    df_temp=df[df.post_process_id==3]
    df_temp['value']=pd.to_numeric(df_temp['value'],errors='coerce')
    df_temp_nona=df_temp.dropna()
    
    # processing difference between temp corrected and observed
    for field in config.temperature_corr_observed_fields:
        compare_observed_corrected(df_temp_nona, field[0], field[1])
    
    # check max temp of a day is always > min temp of day
    for field in config.temperature_min_max_fields:
        compare_min_max(df_temp_nona, field[0], field[1])
        
    # check wet bulb less than temperature observed
    
    # statistical outliers
    tables.populate_error_edit_code(2)
    # get list of annotation ids from error table and remove them from df_temp_nona
    
    
    # get series of values for a given field ID
    for field in config.temperature_stat_outliers:
        flag_outliers(df_temp_nona, field)
    # fit the series
    
    