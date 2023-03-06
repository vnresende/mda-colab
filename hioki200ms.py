import pandas as pd
import numpy as np

def hioki200ms(files):
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
    
    return df_avg


# Using graph_objects
import plotly.express as px

def plot_hioki_graph(df_avg, df_avg_show, title_name, new_labels_name, labels_name, zip_file):
    fig = px.line(df_avg, x = 'datetime', y = df_avg_show.columns,
                hover_data = {'datetime': '| %d/%m \n%H:%M:%S'},
                title = title_name,
                labels = labels_name)
    fig.update_xaxes(tickformat = '%d/%m \n%H:%M:%S')

    fig.for_each_trace(lambda t: t.update(name = new_labels_name[t.name],
                                        legendgroup = new_labels_name[t.name],
                                        hovertemplate = t.hovertemplate.replace(t.name, new_labels_name[t.name])
                                         )
                      )
    #fig.show()
    output_file_name = zip_file + '_' + title_name + '.html'
    fig.write_html(output_file_name)
    return title_name + '.html'


