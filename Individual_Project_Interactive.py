import pandas as pd
import altair as alt
from vega_datasets import data
import streamlit as st

disability_data = pd.read_csv('disability_v2.csv')
df_disability = pd.DataFrame(disability_data)

click = alt.selection_single(fields=['State'])
us_map = alt.Chart(alt.topo_feature(data.us_10m.url, 'states')).mark_geoshape(
).encode(
    alt.Color('Any_Disability:Q', legend=alt.Legend(title='Disability Rate', format='.1%')),
    opacity=alt.condition(click, alt.value(1), alt.value(0.3)),
    tooltip=[alt.Tooltip('State:N', title='State'),
        alt.Tooltip('Any_Disability:Q', title='Disability Rate', format='.1%'),
        alt.Tooltip('Cognitive_Disability:Q', title='Cognitive Disability Rate', format='.1%'),
        alt.Tooltip('Vision_Disability:Q', title='Vision Disability Rate', format='.1%'),
        alt.Tooltip('Hearing_Disability:Q', title='Hearing Disability Rate', format='.1%'),
        alt.Tooltip('Mobility_Disability:Q', title='Mobility Disability Rate', format='.1%'),
        alt.Tooltip('Self_Care_Disability:Q', title='Self Care Disability Rate', format='.1%'),
        alt.Tooltip('Independent_Living_Disability:Q', title='Independent Living Disability Rate', format='.1%')
    ]
).transform_lookup(
    lookup='id',
    from_=alt.LookupData(df_disability, 'id', ['State', 'Any_Disability', 'Cognitive_Disability', 'Vision_Disability', 'Hearing_Disability', 'Mobility_Disability', 'Self_Care_Disability', 'Independent_Living_Disability'])
).project(
    type='albersUsa'
).add_selection(
    click
).properties(
    width=600,
    height=400,
    title='Disability Rate by State'
)




disability_select = alt.binding_select(
    options=[None] + ['Cognitive_Disability', 'Hearing_Disability', 'Mobility_Disability', 'Vision_Disability', 'Self_Care_Disability', 'Independent_Living_Disability'], 
    labels = ['All', 'Cognitive Disability', 'Hearing Disability', 'Mobility Disability', 'Vision Disability', 'Self Care Disability', 'Independent Living Disability'], 
    name='Select')
disability_selection = alt.selection_single(fields=['disability_type'], bind=disability_select)


df_melt = pd.melt(df_disability, id_vars=['Year', 'id', 'abbr', 'State'], var_name='disability_type', value_name='disability_pct')

chart = alt.Chart(df_melt).mark_bar().encode(
    alt.X('State:N', sort=alt.EncodingSortField(
            field='disability_pct', 
            op='max', 
            order='descending')
        ),
    alt.Y('disability_pct:Q', axis=alt.Axis(format='.1%', title='Percentage of People with Disabilities (%)')),
    color=alt.Color('disability_type:N', 
        scale=alt.Scale(domain=[
            'Cognitive_Disability', 'Hearing_Disability', 'Mobility_Disability', 'Vision_Disability', 'Self_Care_Disability', 'Independent_Living_Disability'
            ], 
            scheme='set3'),
        legend=alt.Legend(title='Disability Type')
    ),
    tooltip=['State:N',
        alt.Tooltip('disability_type:N', title='Disability Type'),
        alt.Tooltip('disability_pct:Q', title='Disability Rate', format='.1%')
    ],
    opacity=alt.condition(click, alt.value(1), alt.value(0.3))
).properties(
    width=600,
    height=400,
    title='Proportion of Different Types of Disabilities in Each State'
).add_selection(
    disability_selection
).transform_filter(
    disability_selection
)

interactive = us_map | chart

st.altair_chart(interactive, theme=None)