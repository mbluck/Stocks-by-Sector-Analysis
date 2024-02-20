import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title('Stock Dashboard')

sector = st.selectbox(
    label='Select Sector',
    options=['Technology','Financial Services','Healthcare','Consumer Cyclical', 'Industrials',
             'Communication Services','Consumer Defensive','Energy','Basic Materials','Real Estate','Utilities'],
    index=0
)


# TREEMAP --------
def tree(sector):
    data = pd.read_csv('tree.csv')
    filtered = data[data['Sector'] == sector]
    fig = px.treemap(filtered, 
                 path=['Name'], 
                 values='Market Weight',
                 title='',
                 width=800, height=500,
                 color='Market Weight'
                 )
    fig.data[0].textinfo = 'label+text+value'
    
    fig.update_traces(textfont_size=15, 
                           textposition='middle center',
                           hovertemplate='<b>%{label}</b><br>Market Weight: %{value}',
                           marker_line_width = 0,
                           root_color="#1f2c56")
    
    fig.update_layout(margin=dict(l=0,r=0,b=0,t=0),
                           paper_bgcolor="#1f2c56")
    
    fig.update(layout_coloraxis_showscale=False)

    return fig

st.plotly_chart(tree(sector))