# import getData
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# IMPORT DEFAULT DATA ----------------------------------------

tree_data = pd.read_csv("data/tree.csv")
companies = pd.read_csv("data/companies.csv")

# APP LAYOUT -------------------------------------------------

app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

# setting app.layout = to this function instance allows for the layout to be updated upon every page load, enabling scheduled data updates
def serve_layout():

    return html.Div(
        [
            html.Header(
                [
                    html.H1("Aggregate Stock Data by Sector"),
                    html.H3("Updated daily at NYSE market close, 4:00pm EST"),
                ]
            ),
            html.Main(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H2(
                                        "10 Largest Companies", className="plot_header"
                                    ),
                                    dcc.Dropdown(
                                        id="select_sector",
                                        multi=False,
                                        clearable=True,
                                        value="Technology",
                                        placeholder="Select Sector",
                                        options=[
                                            {"label": c, "value": c}
                                            for c in (tree_data["Sector"].unique())
                                        ],
                                        className="dropdown",
                                    ),
                                    dcc.Graph(
                                        id="companies_list",
                                        config={"displayModeBar": False},
                                        className="plotly_elem",
                                    ),
                                ],
                                id="list",
                            ),
                            html.Div(
                                [
                                    html.H2(
                                        "Market Weights of Industries within Sector (%)",
                                        className="plot_header",
                                    ),
                                    dcc.Graph(
                                        id="sector_treemap",
                                        config={
                                            "displayModeBar": "hover",
                                            "responsive": True,
                                        },
                                        style={"width": "95%", "height": "87%"},
                                        className="plotly_elem",
                                    ),
                                ],
                                id="treemap",
                            ),
                        ],
                        className="row",
                        id="row1",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H2("Price", className="plot_header"),
                                    dcc.Graph(
                                        id="price",
                                        config={
                                            "displayModeBar": False,
                                            "responsive": True,
                                        },
                                        style={"width": "95%", "height": "92%"},
                                        className="plotly_elem",
                                    ),
                                ],
                                className="histogram",
                            ),
                            html.Div(
                                [
                                    html.H2(
                                        "Fifty Day Average", className="plot_header"
                                    ),
                                    dcc.Graph(
                                        id="fifty_avg",
                                        config={
                                            "displayModeBar": False,
                                            "responsive": True,
                                        },
                                        style={"width": "95%", "height": "92%"},
                                        className="plotly_elem",
                                    ),
                                ],
                                className="histogram",
                            ),
                            html.Div(
                                [
                                    html.H2("Stock Volume", className="plot_header"),
                                    dcc.Graph(
                                        id="volume",
                                        config={
                                            "displayModeBar": False,
                                            "responsive": True,
                                        },
                                        style={"width": "95%", "height": "92%"},
                                        className="plotly_elem",
                                    ),
                                ],
                                className="histogram",
                            ),
                        ],
                        className="row",
                        id="row2",
                    ),
                    html.Div(
                        [
                            html.H2("Adjust Histogram Zoom", className="slider_header"),
                            dcc.Slider(
                                id="select_zoom",
                                min=0,
                                max=1,
                                step=0.01,
                                marks=None,
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": True,
                                    "transform": "convertToPercent",
                                },
                                value=0.5,
                                className="slider",
                            ),
                        ],
                        className="slider_container",
                    ),
                ]
            )
        ]
    )


app.layout = serve_layout


# COMPANIES LIST ---------------------------


@app.callback(
    Output(component_id="companies_list", component_property="figure"),
    Input(component_id="select_sector", component_property="value"),
)
def update_companies_list(sector):
    filtered_companies = companies[companies["Sector"] == sector]
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=[""],
                    fill_color="#1f2c56",
                    line_color="#1f2c56",
                    align="center",
                ),
                cells=dict(
                    values=[filtered_companies.Company],
                    fill_color="#1f2c56",
                    line_color="#1f2c56",
                    align="center",
                    height=30,
                ),
            )
        ]
    )
    fig.update_layout(
        font_color="white",
        font_size=18,
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor="#1f2c56",
        height=400,
    )

    return fig


# TREE MAP --------------------------------


@app.callback(
    Output(component_id="sector_treemap", component_property="figure"),
    Input(component_id="select_sector", component_property="value"),
)
def update_tree(sector):
    filtered_tree = tree_data[tree_data["Sector"] == sector]
    fig = px.treemap(filtered_tree, path=["Name"], values="Market Weight", title="")
    fig.data[0].textinfo = "label+text+value"
    fig.data[0]["textfont"]["color"] = "white"

    fig.update_traces(
        textfont_size=15,
        textposition="middle center",
        hovertemplate="<b>%{label}</b><br>Market Weight (%): %{value}",
        marker_line_width=0,
        root_color="#1f2c56",
    )

    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), paper_bgcolor="#1f2c56")

    fig.update(layout_coloraxis_showscale=False)

    return fig


# HISTOGRAMS ------------------------------


@app.callback(
    Output(component_id="price", component_property="figure"),
    [
        Input(component_id="select_sector", component_property="value"),
        Input(component_id="select_zoom", component_property="value"),
    ],
)
def update_price(sector, zoom):
    stocks = pd.read_csv("data/stock_data.csv")
    filtered_stocks = stocks[stocks["Sector"] == sector]
    filtered_stocks = filtered_stocks[filtered_stocks["Price"] != "-1"]

    # to adjust histogram zoom
    new_max = zoom * max(filtered_stocks["Price"])
    new_values = filtered_stocks[filtered_stocks["Price"] <= new_max]

    fig = px.histogram(new_values, x="Price", color_discrete_sequence=["purple"])

    fig.update_layout(
        xaxis_title_text="",
        yaxis_title_text="",
        yaxis={"visible": False, "showticklabels": False},
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor="#1f2c56",
    )
    fig.update_xaxes(
        ticks="outside",
        tickwidth=1,
        tickcolor="white",
        ticklen=5,
        tickfont=dict(color="white", size=14),
    )

    return fig


@app.callback(
    Output(component_id="fifty_avg", component_property="figure"),
    [
        Input(component_id="select_sector", component_property="value"),
        Input(component_id="select_zoom", component_property="value"),
    ],
)
def update_fifty_avg(sector, zoom):
    stocks = pd.read_csv("data/stock_data.csv")
    filtered_stocks = stocks[stocks["Sector"] == sector]
    filtered_stocks = filtered_stocks[filtered_stocks["Fifty Day Average"] != "-1"]

    # to adjust histogram zoom
    new_max = zoom * max(filtered_stocks["Fifty Day Average"])
    new_values = filtered_stocks[filtered_stocks["Fifty Day Average"] <= new_max]

    fig = px.histogram(
        new_values, x="Fifty Day Average", color_discrete_sequence=["purple"]
    )

    fig.update_layout(
        xaxis_title_text="",
        yaxis_title_text="",
        yaxis={"visible": False, "showticklabels": False},
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor="#1f2c56",
    )
    fig.update_xaxes(
        ticks="outside",
        tickwidth=1,
        tickcolor="white",
        ticklen=5,
        tickfont=dict(color="white", size=14),
    )

    return fig


@app.callback(
    Output(component_id="volume", component_property="figure"),
    [
        Input(component_id="select_sector", component_property="value"),
        Input(component_id="select_zoom", component_property="value"),
    ],
)
def update_volume(sector, zoom):
    stocks = pd.read_csv("data/stock_data.csv")
    filtered_stocks = stocks[stocks["Sector"] == sector]
    filtered_stocks = filtered_stocks[filtered_stocks["Volume"] != "-1"]

    # to adjust histogram zoom
    new_max = zoom * max(filtered_stocks["Volume"])
    new_values = filtered_stocks[filtered_stocks["Volume"] <= new_max]

    fig = px.histogram(new_values, x="Volume", color_discrete_sequence=["purple"])

    fig.update_layout(
        xaxis_title_text="",
        yaxis_title_text="",
        yaxis={"visible": False, "showticklabels": False},
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor="#1f2c56",
    )
    fig.update_xaxes(
        ticks="outside",
        tickwidth=1,
        tickcolor="white",
        ticklen=5,
        tickfont=dict(color="white", size=14),
    )

    return fig


# -------- REFRESH DATA ----------------------------------------


def refresh():
    import yahoo_fin.stock_info as si
    import yfinance as yf

    tickers = si.tickers_nasdaq()

    sectors, prices, volumes, fifty_day_averages = (
        [None] * len(tickers) for i in range(4)
    )

    for i, ticker in enumerate(tickers):
        ticker_obj = yf.Ticker(ticker)

        try:
            sector = ticker_obj.info["sector"]
        except:
            sector = -1
        sectors[i] = sector

        try:
            price = ticker_obj.info["currentPrice"]
        except:
            price = str(-1)
        prices[i] = price

        try:
            volume = ticker_obj.info["volume"]
        except:
            volume = str(-1)
        volumes[i] = volume

        try:
            fifty_day_average = ticker_obj.info["fiftyDayAverage"]
        except:
            fifty_day_average = str(-1)
        fifty_day_averages[i] = fifty_day_average

    data_dict = {
        "Ticker": tickers,
        "Sector": sectors,
        "Price": prices,
        "Volume": volumes,
        "Fifty Day Average": fifty_day_averages,
    }

    data = pd.DataFrame(data_dict)
    data.to_csv("data/stock_data.csv", index=False)


# -----------------------------------------------------------------

if __name__ == "__main__":
    app.run_server(debug=True)
