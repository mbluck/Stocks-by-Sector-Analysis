#import getData
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


# IMPORT DEFAULT DATA ----------------------------------------

tree_data = pd.read_csv('default_data/tree.csv')
time_updated = 'Feb 10 2024, 8:31pm'
companies = pd.read_csv('default_data/companies.csv')
stocks = pd.read_csv('default_data/stock_data.csv')

# APP LAYOUT -------------------------------------------------

app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([

	html.Header(
		html.H1("Aggregate Stock Data by Sector")
	),
	
	html.Main([
		html.Div([
			html.Div([
				html.Button("Update Data", id="button"),
				html.Div("Last Updated:", id="last_update")
			], id="button_content")
		], id="button_bar"),
		
		html.Div([
			html.Div([
				html.H2("10 Largest Companies", className="plot_header"),
				dcc.Dropdown(id='select_sector',
                            multi=False,
                            clearable=True,
                            value='Technology',
                            placeholder='Select Sector',
                            options=[{'label': c, 'value': c}for c in (tree_data['Sector'].unique())], 
                            className='dropdown'),
                dcc.Graph(id='companies_list', 
                          config={'displayModeBar': False}, 
                          className='plotly_elem')
			], id="list"),
			html.Div([
				html.H2("Market Weights of Industries within Sector (%)", className="plot_header"),
				dcc.Graph(id='sector_treemap', 
                          config={'displayModeBar': 'hover',
                                  "responsive": True}, 
                          style={'width': '95%', 'height': '87%'},
                          className='plotly_elem')
			], id="treemap"),
		], className="row", id="row1"),
		
		html.Div([
			html.Div([
				html.H2("Price", className="plot_header"),
				dcc.Graph(id='price', 
                            config={'displayModeBar': False,
                                    "responsive": True}, 
                            style={'width': '95%', 'height': '92%'},
                            className="plotly_elem")
			], className="histogram"),
			html.Div([
				html.H2("Price Percent Change", className="plot_header"),
				dcc.Graph(id='per_change', 
                            config={'displayModeBar': False,
                                    "responsive": True}, 
                            style={'width': '95%', 'height': '92%'},
                            className="plotly_elem")
			], className="histogram"),
			html.Div([
				html.H2("Stock Volume", className="plot_header"),
				dcc.Graph(id='volume', 
                            config={'displayModeBar': False,
                                    "responsive": True}, 
                            style={'width': '95%', 'height': '92%'},
                            className="plotly_elem")
			], className="histogram")
		], className="row", id="row2")
	]),
	
	html.Footer()

])

# FETCH NEW DATA ---------------------------
'''
@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    prevent_initial_call=True
    
)
def update_output():
    
    tree_data, companies, time_updated = getData.getTreemapAndListData()
    stocks = getData.getStocksData()
    return tree_data, companies, time_updated, stocks
'''

# COMPANIES LIST ---------------------------

@app.callback(
        Output(component_id='companies_list', component_property='figure'),
        Input(component_id='select_sector', component_property='value')
)

def update_companies_list(sector):
    filtered_companies = companies[companies['Sector'] == sector]
    fig = go.Figure(data=[go.Table(
            header=dict(values=[''],
                    fill_color='#1f2c56',
                    line_color='#1f2c56',
                    align='center'),
            cells=dict(values=[filtered_companies.Company],
                    fill_color='#1f2c56',
                    line_color='#1f2c56',
                    align='center',
                    height=30)
        )
    ])
    fig.update_layout(
            font_color="white",
            font_size=18,
            margin=dict(l=0,r=0,b=0,t=0),
            paper_bgcolor="#1f2c56",
            height=400
    )

    return fig

# TREE MAP --------------------------------

@app.callback(
    Output(component_id='sector_treemap', component_property='figure'),
    Input(component_id='select_sector', component_property='value')
)

def update_tree(sector):
    filtered_tree = tree_data[tree_data['Sector'] == sector]
    fig = px.treemap(filtered_tree, 
                 path=['Name'], 
                 values='Market Weight',
                 title=''
                 )
    fig.data[0].textinfo = 'label+text+value'
    fig.data[0]['textfont']['color'] = 'white'
    
    fig.update_traces(textfont_size=15, 
                           textposition='middle center',
                           hovertemplate='<b>%{label}</b><br>Market Weight (%): %{value}',
                           marker_line_width = 0,
                           root_color="#1f2c56")
    
    fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor="#1f2c56")
    
    fig.update(layout_coloraxis_showscale=False)

    return fig

# HISTOGRAMS ------------------------------

@app.callback(
        Output(component_id='price', component_property='figure'),
        Input(component_id='select_sector', component_property='value')
)

def update_price(sector):
    filtered_stocks = stocks[stocks['Sector']==sector]

    fig = px.histogram(filtered_stocks, x='Price',
                       color_discrete_sequence=['purple'])

    fig.update_layout(
        xaxis_title_text='', 
        yaxis_title_text='',
        yaxis={'visible': False, 'showticklabels': False},
        margin=dict(l=0,r=0,b=0,t=0),
        paper_bgcolor="#1f2c56"
)
    fig.update_xaxes(ticks="outside", tickwidth=1, tickcolor='white', ticklen=5,
                     tickfont=dict(color='white', size=14))

    return fig

@app.callback(
        Output(component_id='per_change', component_property='figure'),
        Input(component_id='select_sector', component_property='value')
)

def update_per_change(sector):
    filtered_stocks = stocks[stocks['Sector']==sector]

    fig = px.histogram(filtered_stocks, x='Percent Change',
                       color_discrete_sequence=['purple'])

    fig.update_layout(
        xaxis_title_text='', 
        yaxis_title_text='',
        yaxis={'visible': False, 'showticklabels': False},
        margin=dict(l=0,r=0,b=0,t=0),
        paper_bgcolor="#1f2c56"
)
    fig.update_xaxes(ticks="outside", tickwidth=1, tickcolor='white', ticklen=5,
                     tickfont=dict(color='white', size=14))

    return fig

@app.callback(
        Output(component_id='volume', component_property='figure'),
        Input(component_id='select_sector', component_property='value')
)

def update_volume(sector):
    filtered_stocks = stocks[stocks['Sector']==sector]

    fig = px.histogram(filtered_stocks, x='Volume',
                       color_discrete_sequence=['purple'])

    fig.update_layout(
        xaxis_title_text='', 
        yaxis_title_text='',
        yaxis={'visible': False, 'showticklabels': False},
        margin=dict(l=0,r=0,b=0,t=0),
        paper_bgcolor="#1f2c56"
)
    fig.update_xaxes(ticks="outside", tickwidth=1, tickcolor='white', ticklen=5,
                     tickfont=dict(color='white', size=14))

    return fig

# -------------------------------------------
    
if __name__ == '__main__':
    app.run_server(debug=True)
