import pandas as pd
import numpy as np

df = []
for file_name in files:
    df.append(pd.read_csv(file_name,  on_bad_lines='skip'))

df_full = pd.concat(df, ignore_index=True)

df_full['Date Time'] = pd.to_datetime(df_full['Date'] + ' ' + df_full['Time'])

shift_column = df_full.pop('Date Time')
df_full.insert(0, 'Date Time', shift_column)

df_dt = pd.DataFrame(df_full['Date Time'])
df_dt.columns = ['datetime'] 

df_full['timestamp'] = df_dt.datetime.values.astype(np.int64) // 10 ** 9
df_dt['timestamp'] = df_full['timestamp']
shift_column = df_full.pop('timestamp')
df_full.insert(1, 'timestamp', shift_column)

df_avg = df_full.groupby('timestamp').mean()

df_avg.reset_index(inplace=True)
df_avg = df_avg.rename(columns = {'index':'timestamp'})

df_avg_datetime = pd.DataFrame(df_avg['timestamp'])
df_avg_datetime['timestamp'] = pd.to_datetime(df_avg_datetime['timestamp'], unit='s')
df_avg_datetime.columns = ['datetime']

df_avg['datetime']= df_avg_datetime['datetime']
df_avg.columns

df_avg_show = pd.DataFrame()
#df_avg_show = df_avg[['Urms1', 'Urms2', 'Umn1', 'Umn2', 'Udc1', 'Udc2', 'Irms1', 'Irms2', 'Imn1', 'Imn2', 'Idc1', 'Idc2']]
df_avg_show = df_avg[['Udc1', 'Udc2', 'Idc1']]
