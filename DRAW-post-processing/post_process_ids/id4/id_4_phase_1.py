import phase1_methods as methods
import tables

def phase_1(entry):
    '''
    Parameters
    ----------
    If the field id is 25, 26, 28 or 29. It represents time.
        Here are my assumptions for the time data. The format must be XX:XX.
            Example 1: the value is '3', it should be transformed to '03:00'
            Example 2: the value is '4':, it should be transformed to '4:00'
            Example 3: the value is '12:345', it should be transformed to '12:34'
            Example 4: the value is '123', it should be transformed to '1:23'
            Example 5: the value is '1234', it should be transformed to '12:34'
            Example 6: the value is '1:2', it should be transformed to '1:20'
            Example 7: the value is '12:4', it should be transformed to '12:40'
            Example 8: the value is '25', it should be transformed to '2:50'
            Example 9: the value is '1:8', it should be transformed to '18:00'
        Here are examples where it is not possible to transform it:
            Example 1: the value is '1:3:00'
            Example 2: the value is ':35'
        It is assigned '?' in such cases
    Returns
    -------
    None.
    
    ERROR CODE ARE NOT UPLOADED !!

    '''
    
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    synonyms_empty = ('empty', 'illegible', 'retracted', 'emptyblank', 'blank')
    #single_letters = ('S', 's', 'T', 't', 'N', 'n', 'R', 'r') #things I noticed that appear by themselves
    inaps = ('inapp', 'inappreciable', 'inap', '?napp', 'napp')
    return_list = list(entry)
    value = entry[1]
    
    if value == None or value == '': #in case missing values
        tables.add_to_corrected_table(*return_list, 0)
        return None
    
    elif value.lower() in inaps: # to unify inaps value
        value= 'inapp'
        return_list[1] = value.lower()
        tables.add_to_corrected_table(*return_list, 0)
        return None
    
    elif value.lower() in synonyms_empty: # if the value was purposely put as problematic
        return_list[1] = value.lower()
        tables.add_to_corrected_table(*return_list, 0)
        return None
    
    else:  #Only deals with values with data in them
        value = value.lower()
        value = value.replace(' ','')
        value = methods.remove_spaces(value, return_list)
        value = methods.correct_double_decimals(value, return_list)
        value = methods.remove_unexpected_characters(value, return_list)
        value = value.replace(";",".")
        value=value.replace("'",'.') #to deal with 3'2
        #value = value.replace('°','')
        #value = value.replace('~','')
        
        if entry[4] in (25,26,28,29): #treat time        
            value=value.replace('.','')
            value=value.replace(',','')
            value=value.replace('(','')
            value=value.replace('&','')
            value=value.replace('/','')
            value=value.replace('-','')
            value=value.replace('_','')
                
            for elements in value: # my way to remove alphabetical characters
                if elements in alphabet:
                    value=value.replace(elements,'')
                elif elements in alphabet.upper():
                    value=value.replace(elements,'')

            if ':' in value: # transform to correct format
                split_data = value.split(':') # to work with data before and after ':'
                if len(split_data)>2: # if there are 2 ':' assign ? 
                    value = '?'
                    return_list[1] = value
                    tables.add_to_corrected_table(*return_list, 0)
                    return None
                
                if len(split_data[0]) == 1: # transform 3:00 to 03:00
                    split_data[0] = '0' + split_data[0]
                    
                elif len(split_data[0])>2: # to deal with 210:00, assign ?
                    value = '?'
                    return_list[1] = value
                    tables.add_to_corrected_table(*return_list, 0)
                    return None
                    
                if len(split_data[1]) == 1: # transform 04:0 to 04:00
                    split_data[1] = split_data[1] + '0'
                    
                elif len(split_data[1])>2: # in case of 09:321, assign ?
                    value = '?'
                    return_list[1] = value
                    tables.add_to_corrected_table(*return_list, 0)
                    return None
                value = ':'.join(split_data[:2]) # put back both halves together
                if value[:2]=='24': #to transform 24:00 to 00:00
                    value = '00'+':'+value[3:]
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
                return None
            
            
            elif len(value) == 1: # single digit case, i.e 7 to 07:00
                value = '0' + value + ':00'
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
                return None
            
            elif len(value) == 2: # two digit case
                if int(value[:2])>24: # in case of 32, assign 03:20
                    value = '0'+value[0]+':'+value[1]+'0'
                    return_list[1] = value
                    tables.add_to_corrected_table(*return_list, 0)
                    return None
                if value[:2]=='24': # avoid 24:00 and put 00:00
                    value = '00:00'
                    return_list[1] = value
                    tables.add_to_corrected_table(*return_list, 0)
                    return None
        
                value = value + ':00' # transform 22 to 22:00
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
                return None
            
            elif len(value) == 3: # three digit case, 320 to 03:20
                value ='0' + value[0] + ':' + value[1:]
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
                return None
                
            elif len(value) == 4: # four digit case
                if int(value[:2]) > 24: # i.e 4321 should be 04:32
                    value = '0'+value[0]+':'+value[1:3]
                    return_list[1] = value
                    tables.add_to_corrected_table(*return_list, 0)
                    return None
                elif value[:2]=='24': # avoid 24:00 and put 00:00
                    value = '00'+':'+value[2:]
                    return_list[1] = value
                    tables.add_to_corrected_table(*return_list, 0)
                    return None
                else:
                    value = value[:2] + ':' + value[2:] #transform 1621 to 16:21
                    return_list[1] = value
                    tables.add_to_corrected_table(*return_list, 0)
                    return None
                
            elif len(value)>4: #12345
                if value[:2]=='24': # avoid 24:00 and put 00:00
                    value = '00'+':'+value[2:4]
                    return_list[1] = value
                    tables.add_to_corrected_table(*return_list, 0)
                    return None
                else:
                    value = value[:2]+':'+value[2:4] # cut the last digit
                    return_list[1] = value
                    tables.add_to_corrected_table(*return_list, 0)
                    return None
            else:
                return_list[1] = value
                tables.add_to_corrected_table(*return_list, 0)
                return None
            
        
       # else:
            #No longer time
        value=value.replace(',','.')         
        value = value.replace('/','0')
        value = value.replace('-','0')
        if len(value)>0:  
            if value[0]=='.': # to avoid .6 and put 0.6
                value='0'+value
            if value[-1]=='.': # to avoid 6. and put 6.0
                value=value+'0'
        return_list[1] = value
        tables.add_to_corrected_table(*return_list, 0)
        return None
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
