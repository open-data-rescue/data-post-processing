
import pandas as pd
import tables
import config
import math
#import numpy as np
# curve-fit() function imported from scipy
#from scipy.optimize import curve_fit
from matplotlib import pyplot as plt


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
    log_errors('302', errors_date_temp)    



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
            log_errors('303', entries_date)
   
  
   
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

    

def flag_outliers (df, field_id):
    # Test function with coefficients as parameters
    def test(x, a, b,c,d,e,f):
        return a * x*x*x*x*x +b*x*x*x*x +c*x*x*x+d*x*x+e*x+f

    df_proc=df[df.field_id==field_id].sort_values(by=['observation_date'])
    df_proc.reset_index(inplace=True)
    
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
                outliers=df_proc[df_proc.index.isin(delta[delta.gt(5*standard_deviation)].index)]
                if outliers.size >0:
                    plt.plot(x, y, '.', color ='black', label ="data")
                    plt.plot(x, ans, '--', color ='blue', label ="rolling mean")
                    plt.plot(outliers.observation_date, outliers.value,'o', color='red', label="Outliers")
                    plt.title("Field: " +str(field_id))
                    plt.legend()
                    plt.show()
                    # do something with the outliers
            obs_date=row['observation_date']
            list_partial=[]
            list_partial.append(row)
#  error code = 025
            
            
            # # Get list of months for outliers
            # for outlier_year_month in (outliers.observation_date.dt.to_period('M').unique()):
            #     df_mon=df_proc[df_proc.observation_date.dt.to_period('M')==outlier_year_month]
            #     outliers_mon=outliers[outliers.observation_date.dt.to_period('M')==outlier_year_month]
            #     x=df_mon.observation_date
            #     y=df_mon.value
            #     ans_mon=ans[ans.index.isin(x.index)]
            #     plt.plot(x, y, '.', color ='black', label ="data")
            #     plt.plot(x, ans_mon, '--', color ='blue', label ="rolling mean")
            #     plt.plot(outliers_mon.observation_date, outliers_mon.value,'o', color='red', label="Outliers")
            #     plt.title("Field: " +str(field_id)+" - "+str(outlier_year_month))
            #     plt.legend()
            #     plt.show()   




def phase_2(entries,debug=False):
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
    if debug==False: 
        tables.populate_error_edit_code(2)
        # get list of annotation ids from error table and remove them from df_temp_nona
        annotations=tables.get_error_code_annotations('2','3')
        df_temp_cleaned=df_temp_nona[~df_temp_nona.annotation_id.isin(annotations)]
    else:
        df_temp_cleaned=df_temp_nona
    
    # get series of values for a given field ID
    for field in config.temperature_stat_outliers:
        flag_outliers(df_temp_cleaned, field)
    # fit the series
    
    