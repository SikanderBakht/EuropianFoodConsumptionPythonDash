import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_html_components.Div import Div
from dash_html_components.H5 import H5
from dash_html_components.P import P
import plotly.express as px
import urllib.request as urllib
import os
import dash_bootstrap_components as dbc

# from urllib.request import urlopen
import pandas as pd
import plotly.graph_objs as go
import statsmodels.api as sm
import plotly.figure_factory as ff
import numpy as np

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

food_options_ = [
    "Alcoholic Beverages",
    "Animal fats",
    "Cereals - Excluding Beer",
    "Eggs",
    "Fish, Seafood",
    "Fruits - Excluding Wine",
    "Meat",
    "Milk - Excluding Butter",
    "Offals",
    "Oilcrops",
    "Pulses",
    "Spices",
    "Starchy Roots",
    "Stimulants",
    "Sugar & Sweeteners",
    "Treenuts",
    "Vegetable Oils",
    "Vegetables",
]

mapbox_access_token = "pk.eyJ1Ijoic3RlZmZlbmhpbGwiLCJhIjoiY2ttc3p6ODlrMG1ybzJwcG10d3hoaDZndCJ9.YE2gGNJiw6deBuFgHRHPjg"
path = "https://raw.githubusercontent.com/FranzMichaelFrank/health_eu/main/"
df = pd.read_csv(path + "food_supply.csv", dtype={"id": str})
df_scatter = pd.read_csv(path + "scatter_data.csv", dtype={"id": str})
url = path + "european-union-countries.geojson"
response = urllib.urlopen(url)
european_union = json.loads(response.read())
health = df_scatter[
    [
        "Country",
        "Obesity",
        "Diabetes Prevalence",
        "Cardiovascular Death Rate",
        "Life Expectancy",
        "Health Expenditure",
    ]
]

health_cols = [
    "Obesity",
    "Diabetes Prevalence",
    "Cardiovascular Death Rate",
    "Life Expectancy",
    "Health Expenditure",
]
# print(df_scatter)
# print(health)

fig_bar = go.Figure()
fig_bar.add_trace(
    go.Bar(
        x=health["Country"], y=health["Obesity"], name="Obesity", marker_color="#0d0887"
    )
)
fig_bar.add_trace(
    go.Bar(
        x=health["Country"],
        y=health["Diabetes Prevalence"],
        name="Diabetes Prevalence",
        marker_color="#7201a8",
    )
)

fig_bar.add_trace(
    go.Bar(
        x=health["Country"],
        y=health["Cardiovascular Death Rate"],
        name="Cardiovascular Death Rate",
        marker_color="#bd3786",
    )
)

fig_bar.add_trace(
    go.Bar(
        x=health["Country"],
        y=health["Life Expectancy"],
        name="Life Expectancy",
        marker_color="#ed7953",
    )
)

fig_bar.add_trace(
    go.Bar(
        x=health["Country"],
        y=health["Health Expenditure"],
        name="Health Expenditure",
        marker_color="#fdca26",
    )
)


food_options = [dict(label=country, value=country)
                for country in food_options_]

radio_food_behaviour = dcc.RadioItems(
    id="nutrition_types",
    options=food_options,
    value="Alcoholic Beverages",
    labelStyle={"display": "block", "textAlign": "justify"},
)

corr_options = [
    dict(label=disease, value=disease)
    for disease in [
        "Obesity",
        "Diabetes Prevalence",
        "Cardiovascular Death Rate",
        "Life Expectancy",
        "Health Expenditure",
    ]
]

cor_behav = dcc.Dropdown(
    id="cor_behave",
    options=corr_options,
    value="Obesity"
)

# region app layout
app.layout = html.Div([
    html.H2('Food consumption characteristics of the European Union', style={
            "fontWeight": "bold", 'textAlign': 'center', 'marginTop': '100px'}),
    html.H4('Analysis of the relationship between nutritional patterns and the health status within the countries', style={
            'textAlign': 'center'}),
    html.Div([
        # region food type selection layout
        html.Div([
            html.H6('Consumption by food type', style={
                'textAlign': 'center', 'fontWeight': 'bold'}),
            html.P('The cultures and customs of the 27 EU countries differ widely. The same applies to their eating and drinking habits. The map on the right explores the food supply in kilograms per capita per year.', style={
                   'textAlign': 'center'}),
            html.P(
                "Select a food category",
                className="control_label",
                style={"textAlign": "center",
                       "fontWeight": "bold"},
            ),
            radio_food_behaviour

        ], style={'padding': '10px', 'marginRight': '50px'},
            className='card col-4',
            id='food-type'),
        # endregion

        html.Div([
            html.Div([
                # region min, max, standard deviation
                html.Div([
                    html.Div([
                        html.P(
                            "Maximum",
                            style={
                                "textAlign": "center",
                                "fontWeight": "bold",
                            },
                        ),
                        html.P(
                            id="max_name",
                            style={"textAlign": "center"},
                        ),
                        html.P(
                            id="max_value",
                            style={"textAlign": "center"},
                        ),
                    ], style={'padding': '10px', 'marginRight': '20px'},
                        className='card col',
                        id='max-consumption'),

                    html.Div([
                        html.P(
                            "Minimum",
                            style={
                                "textAlign": "center",
                                "fontWeight": "bold",
                            },
                        ),
                        html.P(
                            id="min_name",
                            style={"textAlign": "center"},
                        ),
                        html.P(
                            id="min_value",
                            style={"textAlign": "center"},
                        ),
                    ], style={'padding': '10px', 'marginRight': '20px'},
                        className='card col',
                        id='min-consumption'),

                    html.Div([
                        html.P(
                            "Mean",
                            style={
                                "textAlign": "center",
                                "fontWeight": "bold",
                            },
                        ),
                        html.P(
                            id="mean", style={"textAlign": "center"}
                        ),
                        html.P(
                            "Standard deviation",
                            style={
                                "textAlign": "center",
                                "fontWeight": "bold",
                            },
                        ),
                        html.P(
                            id="st_dev", style={"textAlign": "center"}
                        ),
                    ], style={'padding': '10px'},
                        className='card col',
                        id='std-consumption'),
                ], className='row'),
                # endregion
            ], className='col'),

            html.Div(
                [dcc.Graph(id="choropleth")],
                # id="countGraphContainer",
                className="card", style={'marginTop': '10px', 'width': '100%', 'padding': '20px'}
            )
        ], className='col-7'),
    ], className='row', style={'width': '100%'}),

    html.Div([
        html.H6('General health information about the countries', style={
                'textAlign': 'center', 'fontWeight': 'bold'}),
        html.P(
            "Similarly to nutrition, the health status also varies from country to country. The bar chart below shows the differences between the countries in terms of the following variables: prevalence of obesity in the adult population in % (Obesity), prevalence of diabetes in the adult population in % (Diabetes Prevalence), cardiovascular death rate per 100,000 population (Cardiovascular Death Rate), average life expectancy in years (Life Expectancy) and the expenditure of the government on the country's health system in % of the respective GDP (Health Expenditure).",
            style={
                'textAlign': 'center'
            }),
        html.Div(
            [dcc.Graph(id="bar_chart", figure=fig_bar)],
            className="pretty_container twelve columns",
        ),
    ], className='card row', style={'width': '100%', 'padding': '20px'}),

    html.Div([
        html.Div([
            html.H6('Exploring correlations', style={
                    'textAlign': 'center', 'fontWeight': 'bold'}),
            html.P(
                "In the heatmap below, the correlations between the 5 health variables and the 18 food variables can be explored.",
                style={
                    'textAlign': 'center'
                }),
            html.P(
                "Select a health variable",
                className="control_label",
                style={"textAlign": "center",
                       "fontWeight": "bold"},
            ),
            cor_behav,
            html.Div(
                [dcc.Graph(id="cor_ma")],
                className="pretty_container twelve columns",
            ),
        ], className='card col-4'),
        html.Div([
            html.H6('Analysing the correlations between food consumption and health', style={
                    'textAlign': 'center', 'fontWeight': 'bold'}),
            html.P(
                "Below, the correlations can be analysed in more detail. It is important to note that correlation in this case does not necessarily mean causation. For example, the wealth level of a country might often influence the variables, which is why it is represented through the size of the dots as GDP per capita. Furthermore, outliers should also be watched out for.",
                style={
                    'textAlign': 'center'
                }),
            html.Div([
                html.Div(
                    [
                        html.P(
                            "Select a food category",
                            style={
                                "font-weight": "bold",
                                "text-align": "center",
                            },
                        ),
                        dcc.Dropdown(
                            id="xaxis-column",
                            options=[
                                {"label": i, "value": i} for i in food_options_
                            ],
                            value="Alcoholic Beverages",
                        ),
                    ],
                    className='col'
                ),
                html.Div(
                    [
                        html.P(
                            "Select a health variable",
                            style={
                                "font-weight": "bold",
                                "text-align": "center",
                            },
                        ),
                        dcc.Dropdown(
                            id="yaxis-column",
                            options=[
                                {"label": i, "value": i} for i in health_cols
                            ],
                            value=health_cols[0],
                        ),
                    ],
                    className='col'
                )
            ], className='row'),

            html.Div(
                [dcc.Graph(id="indicator-graphic"), ],
            ),

        ], className='card col-7')
    ], className='row', style={'width': '100%'}),

    html.Div([
        html.H6('K-means clustering',
                style={
                    'textAlign': 'center', 'fontWeight': 'bold'
                },
                ),
        html.P(
            "Below, the correlations can be analysed in more detail. It is important to note that correlation in this case does not necessarily mean causation. For example, the wealth level of a country might often influence the variables, which is why it is represented through the size of the dots as GDP per capita. Furthermore, outliers should also be watched out for.",
            style={
                'textAlign': 'center'
            }),
    ], className='row card', style={'width': '100%'})
], style={'padding': '50px'})
# endregion

# region callbacks


@app.callback(
    [
        Output("max_name", "children"),
        Output("max_value", "children"),
        Output("min_name", "children"),
        Output("min_value", "children"),
        Output("mean", "children"),
        Output("st_dev", "children"),
    ],
    [Input("nutrition_types", "value"), ],
)
def indicator(auswahl):
    max_id = df[auswahl].idxmax()
    min_id = df[auswahl].idxmin()

    max_value = df[auswahl].max()
    max_value = str(max_value)

    max_name = df.loc[max_id, "Country"]
    min_value = df[auswahl].min()
    min_value = str(min_value)

    min_name = df.loc[min_id, "Country"]
    mean = df[auswahl].mean()
    st_dev = df[auswahl].std()
    st_dev = round(st_dev, 2)
    st_dev = str(st_dev)
    mean = round(mean, 2)
    mean = str(mean)

    return (
        "Country: " + max_name,
        max_value + " kg per capita per year",
        "Country: " + min_name,
        min_value + " kg per capita per year",
        mean + " kg per capita per year",
        st_dev + " kg per capita per year",
    )


@app.callback(Output("choropleth", "figure"), [Input("nutrition_types", "value")])
def display_choropleth(candi):
    fig = px.choropleth_mapbox(
        df,
        geojson=european_union,
        color=candi,
        locations="iso_a3",
        featureidkey="properties.gu_a3",
        hover_name="Country",
        opacity=0.7,  # hover_data = [],
        center={"lat": 56.5, "lon": 11},
        zoom=2.5,
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}, mapbox_accesstoken=mapbox_access_token
    )

    return fig


@app.callback(Output("cor_ma", "figure"), [Input("cor_behave", "value")])
def display_cor_ma(var):
    foods_health = [
        "Vegetables",
        "Vegetable Oils",
        "Treenuts",
        "Sugar & Sweeteners",
        "Stimulants",
        "Starchy Roots",
        "Spices",
        "Pulses",
        "Oilcrops",
        "Offals",
        "Milk - Excluding Butter",
        "Meat",
        "Fruits - Excluding Wine",
        "Fish, Seafood",
        "Eggs",
        "Cereals - Excluding Beer",
        "Animal fats",
        "Alcoholic Beverages",
        "Obesity",
        "Diabetes Prevalence",
        "Cardiovascular Death Rate",
        "Life Expectancy",
        "Health Expenditure",
    ]

    df_corr_r = df_scatter[foods_health]
    df_corr_round = df_corr_r.corr()[[var]].round(2)
    # , "Diabetes Prevalence", "Cardiovascular Death Rate", "Life Expectancy", "Health Expenditure"
    fig_cor = ff.create_annotated_heatmap(
        z=df_corr_round.to_numpy(),
        x=df_corr_round.columns.tolist(),
        y=df_corr_round.index.tolist(),
        zmax=1,
        zmin=-1,
        showscale=True,
        hoverongaps=True,
        ygap=3,
    )
    fig_cor.update_layout(
        yaxis=dict(showgrid=False),
        xaxis=dict(showgrid=False),
        legend=dict(orientation="h", yanchor="bottom",
                    y=1.02, xanchor="right", x=1),
    )
    # fig_cor.update_layout(yaxis_tickangle=-45)
    fig_cor.update_layout(xaxis_tickangle=0)
    fig_cor.update_layout(title_text="", height=550)  #

    return fig_cor
# endregion


@app.callback(
    Output("indicator-graphic", "figure"),
    Input("xaxis-column", "value"),
    Input("yaxis-column", "value"),
)
def update_graph(xaxis_column_name, yaxis_column_name):

    # col_name = str(yaxis_column_name) + " (above Average)"
    col_name = " "
    df_scatter[col_name] = (
        df_scatter[yaxis_column_name] > df_scatter[yaxis_column_name].mean()
    )

    def aa(inp):
        if inp == True:
            return yaxis_column_name + " above average"
        else:
            return yaxis_column_name + " below average"

    df_scatter[col_name] = df_scatter[col_name].apply(aa)

    fig = px.scatter(
        df_scatter,
        x=xaxis_column_name,
        y=yaxis_column_name,
        size="GDP per Capita",
        color=col_name,
        hover_name="Country",
        log_x=False,
        template="simple_white",
        color_discrete_sequence=["#0d0887", "#9c179e"],
    )

    # linear regression
    regline = (
        sm.OLS(
            df_scatter[yaxis_column_name],
            sm.add_constant(df_scatter[xaxis_column_name]),
        )
        .fit()
        .fittedvalues
    )

    # add linear regression line for whole sample
    fig.add_traces(
        go.Scatter(
            x=df_scatter[xaxis_column_name],
            y=regline,
            mode="lines",
            marker_color="#fb9f3a",
            name="OLS Trendline",
        )
    )

    fig.update_layout(
        legend=dict(orientation="h", xanchor="center",
                    x=0.5, yanchor="top", y=-0.2)
    )

    fig.update_layout(
        margin={"l": 40, "b": 40, "t": 10, "r": 0}, hovermode="closest")

    # fig.update_xaxes(title=xaxis_column_name,
    #                type='linear' if xaxis_type == 'Linear' else 'log')

    # fig.update_yaxes(title=yaxis_column_name,
    #                type='linear' if yaxis_type == 'Linear' else 'log')

    return fig


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
