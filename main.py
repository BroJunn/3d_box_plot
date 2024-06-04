import pandas as pd
import plotly.graph_objects as go
import numpy as np

file_path = 'rest.csv'
df_raw = pd.read_csv(file_path)

group = 'group'
group_values = [0, 1, 2]
time = 'time'
time_values = ['time0', 'time1', 'time2', 'time3']

group = []
time = []
value = []

for group_value in group_values:
    for time_value in time_values:
        filtered_df = df_raw[(df_raw['group'] == group_value) & (df_raw['time'] == time_value)]['painscore'].to_numpy()
        group += [group_value] * len(filtered_df)
        time += [time_value] * len(filtered_df)
        value += list(filtered_df)

data = {
    'group': group,
    'time': time,
    'value': value
}


df = pd.DataFrame(data)

fig = go.Figure()

times = ['time0', 'time1', 'time2', 'time3']
groups = [0, 1, 2]

colors = ['#636EFA', '#EF553B', '#00CC96']

for g_idx, group in enumerate(groups):
    for t_idx, time in enumerate(times):
        filtered_df = df[(df['group'] == group) & (df['time'] == time)]
        values = filtered_df['value']

        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        median = np.median(values)
        iqr = q3 - q1
        whisker_low = q1 - 1.5 * iqr
        whisker_high = q3 + 1.5 * iqr
        whisker_low = max(whisker_low, values.min())
        whisker_high = min(whisker_high, values.max())

        fig.add_trace(go.Scatter3d(
            x=[time, time], z=[whisker_low, whisker_high], y=[group, group],
            mode='lines', line=dict(color=colors[g_idx], width=2), showlegend=False
        ))
        fig.add_trace(go.Scatter3d(
            x=[time, time], z=[q1, q3], y=[group, group],
            mode='markers', marker=dict(color=colors[g_idx], size=10), showlegend=False
        ))
        fig.add_trace(go.Scatter3d(
            x=[time], z=[median], y=[group],
            mode='markers', marker=dict(color='black', size=5), showlegend=False
        ))

fig.update_layout(
    title='3D Box Plot of Pain Scores over Time',
    scene=dict(
        xaxis=dict(title='Time', tickvals=list(range(len(times))), ticktext=times),
        zaxis=dict(title='Pain Score'),
        yaxis=dict(title='Group', tickvals=groups, ticktext=['0', '1', '2']),
    )
)

fig.show()
