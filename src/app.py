"""dsfds."""
import dash
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc

import plotly.express as px

import pynch.mass_table as mt

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

df = mt.MassTable().full_data

table_years = df.index.unique()
variables = df.columns

segre_colours = {
    'stable': 'black',
    'B-': 'red',
    'B+': 'blue',
    'A': 'yellow',
    'n': 'limegreen',
    '2n': 'darkgreen',
    'p': 'magenta',
    '2p': 'purple',
    'EC': 'orange',
    'SF': 'cyan'
}


@app.callback(
    [
        Output("graph-title", "children"),
        Output("a-graph", "figure"),
        Output("z-graph", "figure"),
        Output("n-graph", "figure"),
        Output("xval_slider", "min"),
        Output("xval_slider", "max"),
        Output("xval_slider", "marks"),
    ],
    [
        Input("yaxis_dropdown", "value"),
        Input("xval_slider", "value"),
        Input("year_slider", "value"),
    ],
)
def update_graph(y_var, x_value, year):
    """The actions to do when the selected data is changed."""
    df_f = df.loc[table_years[year]][["Symbol", "Decay", "A", "Z", "N", y_var]]
    df_ff = df_f.loc[(df_f["A"] == x_value)]

    logit = (
        True
        if y_var in ["HalfLife", "NUBASERelativeError", "AMERelativeError"]
        else False
    )

    a_fig = px.scatter(
        data_frame=df_f,
        x="N",
        y="Z",
        hover_name="Symbol",
        color="Decay",
        color_discrete_map=segre_colours,
        template="plotly_dark",
    )

    z_fig = px.scatter(
        data_frame=df_ff,
        x="Z",
        y=y_var,
        hover_name="Symbol",
        hover_data=[y_var],
        log_y=logit,
        template="plotly_dark",
    )

    n_fig = px.scatter(
        data_frame=df_ff,
        x="N",
        y=y_var,
        hover_name="Symbol",
        hover_data=[y_var],
        log_y=logit,
        template="plotly_dark",
    )

    title = dash.html.H2(f"A = {x_value}")

    min_a = df_f["A"].min()
    max_a = df_f["A"].max()

    marks_a = {i: f"{i}" for i in range(20, max_a, 20)}

    return (
        title,
        a_fig,
        z_fig.update_traces(mode="lines+markers"),
        n_fig.update_traces(mode="lines+markers"),
        min_a,
        max_a,
        marks_a,
    )


year_and_variable = dbc.Row(
    [
        dbc.Col(
            dash.html.Div(
                [
                    dash.html.H3("Year"),
                    dash.dcc.Slider(
                        id="year_slider",
                        min=0,
                        max=len(table_years) - 1,
                        marks={i: f"{table_years[i]}" for i in range(len(table_years))},
                        value=0,
                    ),
                ],
            )
        ),
        dbc.Col(
            dash.html.Div(
                [
                    dash.html.H3("Value to plot"),
                    dash.dcc.Dropdown(
                        id="yaxis_dropdown",
                        options=[{"label": i, "value": i} for i in variables],
                        value=variables[7],
                    ),
                ],
            )
        ),
    ]
)

a_slider = dbc.Row(
    dbc.Col(
        [
            dash.html.Div(id="graph-title", children=[]),
            dash.html.Div(dash.dcc.Slider(id="xval_slider", value=50)),
        ]
    )
)

graphs = dbc.Row(
    [
        dbc.Col(dash.dcc.Graph(id="n-graph", figure={}), width=3),
        dbc.Col(dash.dcc.Graph(id="a-graph", figure={}), width=6),
        dbc.Col(dash.dcc.Graph(id="z-graph", figure={}), width=3),
    ]
)


app.layout = dbc.Container(children=[year_and_variable, graphs, a_slider], fluid=True)


def main():
    """For testing."""

    # df = MassData().full_data
    # print(df)
    # print(df.index.unique())
    # print(df.columns)
    # print(df.loc['2003', ['A', 'Symbol']])
    # print(df.loc[(df['Z'] == 2) & (df['A'] == 3) & (df['TableYear'] == '2003')])
    # print(df.loc['2003'][['A', 'Z']])
    # df_f = df.loc["2003"][["A", "Z", "N", "NubaseRelativeError"]]
    # df_ff = df_f.loc[(df_f["A"] == 12)]
    # print(df_ff)
    # print(df_ff["Z"].max())
    # print(df_ff["Z"].min())
    # print(df_f.loc[(df_f['A'] == 20)])
    # filtered = df[df["TableYear"] == "2003"]
    # print(filtered)
    # print(type(filtered))

    # print(df.loc[(25), :]['2012']['NubaseMassExcess'].index.get_level_values('N'))
    # print("~~~~~~~~~~~~~~~~~~~~~~")
    # print(df[df.index.get_level_values('A') == 40]['2016']['NubaseMassExcess'])
    # print("~~~~~~~~~~~~~~~~~~~~~~")
    # print(df.loc[(40), :]["2016"]["NubaseMassExcess"])


if __name__ == "__main__":
    # main()
    app.run_server(debug=True)
