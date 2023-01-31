import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

# Iris bar figure


def drawFigure():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.bar(
                        df, x="sepal_width", y="sepal_length", color="species"
                    ).update_layout(
                        template='plotly_dark',
                        plot_bgcolor='rgba(0, 0, 0, 0)',
                        paper_bgcolor='rgba(0, 0, 0, 0)',
                    ),
                    config={
                        'displayModeBar': False
                    }
                )
            ])
        ),
    ])

# Text field


def drawText():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Text"),
                ], style={'textAlign': 'center'})
            ])
        ),
    ])


# Data
df = px.data.iris()

# Build App
app = JupyterDash(external_stylesheets=[dbc.themes.SLATE])


app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    drawText()
                ], width=3),
                dbc.Col([
                    drawText()
                ], width=3),
                dbc.Col([
                    drawText()
                ], width=3),
                dbc.Col([
                    drawText()
                ], width=3),
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawFigure()
                ], width=3),
                dbc.Col([
                    drawFigure()
                ], width=3),
                dbc.Col([
                    drawFigure()
                ], width=6),
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([drawFigure()], width=9),
                dbc.Col([
                    dbc.Row([drawFigure()]),
                    dbc.Row([drawFigure()])]
                )
                # dbc.Col([drawFigure()], width=3),
                # dbc.Col('asd')
            ], align='center'),
        ]), color='dark'
    )
])

app.layout = dbc.Container([
    dbc.Col([
        dbc.Row([
            dbc.Col(drawFigure()),
            dbc.Col(drawFigure()),
            dbc.Col(drawFigure())]
        ),
        dbc.Row(drawFigure())], width=4
    ),
    dbc.Col([dbc.Row(drawFigure())

             ], width=6, style = 'display : inline-block')], fluid=True)



app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("2", style={"height": "50%"}, className="border"),
                        html.Div("3", style={"height": "50%"}, className="border"),
                    ],
                    width=7,
                ),
                dbc.Col(html.Div("1", className="vh-100 border")),
            ],
            className="g-0",
        )
    ],
    fluid=True,
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row([dbc.Col(['Testing']), dbc.Col(['Testing']), dbc.Col(['Testing'])]
                        
                        
                        
                        , style={"height": "50%"}, className="g-0 border"),
                        html.Div("3", style={"height": "50%"}, className="border"),
                    ],
                    width=7,
                ),
                dbc.Col(html.Div("1", className="vh-100 border")),
            ],
            className="g-0",
        )
    ],
    fluid=True,
)


app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row([dbc.Col([drawFigure()]), dbc.Col([drawFigure()]), dbc.Col([drawFigure()])]
                        
                        
                        
                        , style={"height": "50%"}, className="g-0 border"),
                        html.Div(drawFigure(), style={"height": "50%"}, className="border"),
                    ],
                    width=7,
                ),
                dbc.Col(html.Div(drawFigure(), className="vh-100 border")),
            ],
            className="g-0",
        )
    ],
    fluid=True,
)

# app.layout = html.Div([
#     dbc.Card(
#         dbc.CardBody([
#             dbc.Col([
#                 dbc.Row([
#                     dbc.Col(drawFigure()),
#                     dbc.Col(drawFigure()),
#                     dbc.Col(drawFigure())]
#                 ),
#                 dbc.Row(drawFigure())], width=4
#             ),
#             dbc.Col([dbc.Row(drawFigure())

#             ])


#         ]


#         ))])
# Run app and display result inline in the notebook
app.run_server(mode='external', debug=True)
