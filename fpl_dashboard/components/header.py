import dash_html_components as html
import dash_core_components as dcc


def header():
    return html.Div([
        get_title(),
        html.Br([]),
        get_menu(),
    ])


def get_title():
    title = html.Div([

        html.Div([
            html.H2(children='Fantasy Football Dashboard',
                    style={'textAlign': 'center'})
        ], style={'margin-top': 'auto', 'margin-bottom': 'auto'})

    ], className="eight columns",
        style={'float': 'left', 'position': 'relative', 'overflow': 'auto'})
    return title


def get_menu():
    menu = html.Div(children=[
        html.Nav(children=[
            html.Ul(children=[
                html.Li(dcc.Link('Summary', href='/fpl-dashboard/summary')),
                html.Li(dcc.Link('Summary', href='/fpl-dashboard/player_compare')),
            ])
        ])
    ], className="twelve columns",
        style={'float': 'left', 'position': 'relative', 'margin-bottom': 30})

    return menu
