## Create DataFrame from Statistics Canada Table

import pandas as pd
import urllib.parse
import textwrap


# This script demonstrates how to download a CSV file from the Statistics Canada website
# using the downloadDbLoadingData-nonTraduit.action endpoint.
def create_df_sc(pid,start_date,selected_members,period,latest_n="",end_date=""):
    base_url = "https://www150.statcan.gc.ca/t1/tbl1/en/dtl!downloadDbLoadingData-nonTraduit.action"
    pid = pid
    latestN =  latest_n
    startDate = start_date
    endDate = end_date
    csvLocale = "en"
    selected_members = selected_members

    #encode selected members
    encoded_selected_members = urllib.parse.quote(selected_members,safe='')

    # Construct the full URL
    url = "{}?pid={}&latestN={}&startDate={}&endDate={}&csvLocale={}&selectedMembers={}" \
        .format(base_url,pid,latestN,startDate,endDate,csvLocale,encoded_selected_members)

    # Print the URL
    print(url,'\n')
    
    # Read the CSV data into a DataFrame
    df = pd.read_csv(url)
    
    # drop extra columns
    columns_to_drop = ['DGUID', 'COORDINATE', 'UOM', 'SCALAR_FACTOR',
        'UOM_ID','SCALAR_ID','VECTOR', 'STATUS', 'SYMBOL', 'TERMINATED', 'DECIMALS']
    
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], axis=1)
    
    # convert the 'REF_DATE' column to a datetime object
    df['REF_DATE']=pd.to_datetime(df['REF_DATE'])
    
    # set the 'REF_DATE' column as the index
    df.set_index('REF_DATE', inplace=True)

    # convert the index to a period index
    # removed: causes error in seaborn plots
    # df.index = df.index.to_period(period)
    
    #display df
    print(df.info(),'\n')
    print(df.tail())
    
    return df

'''
# Test def create_df_sc
pid = "1410028701"
start_date = "20190101"
selected_members = "[[1,2,3],[1,2,3,4,5,6,7,8,9],[1],[1],[1],[1]]"
period = 'M'
df = create_df_sc(pid,start_date,selected_members,period)
'''



def wrap_labels(ax, width, break_long_words=False):
    labels = []
    for label in ax.get_xticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width,
                      break_long_words=break_long_words))
    ax.set_xticklabels(labels, rotation=0)

