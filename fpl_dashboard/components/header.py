import dash_html_components as html
import dash_core_components as dcc


def header():
    return html.Div([
        get_fill(),
        get_title(),
        get_logo(),
        html.Br([]),
        # get_menu()
    ])


def get_fill():
    return html.Div(
        className="two columns",
        style={'height': 100}
    )


def get_logo():
    logo = html.Div([
                html.Div([
                    html.Span([], className="helper"),
                    html.Img(src='/static/creme-logo-180.png'),
                ], style={'float': 'left', 'height': 100}),
            ], className="two columns", id='logos',
        style={'float': 'left', 'position': 'relative', 'height': 100, 'text-align': 'center'})

    return logo


def get_title():
    title = html.Div([

        html.Div([
            html.H2(children='Microbiome Dashboard',
                    style={'textAlign': 'center'})
        ], style={'margin-top': 'auto', 'margin-bottom': 'auto'})

    ], className="eight columns",
        style={'float': 'left', 'position': 'relative', 'overflow': 'auto'})
    return title


def get_menu():
    menu = html.Div(children=[
        html.Nav(children=[
            html.Ul(children=[
                html.Li(dcc.Link('Summary', href='/microbiome-dashboard/summary')),
            ])
        ])
    ], className="twelve columns",
        style={'float': 'left', 'position': 'relative', 'margin-bottom': 30})

    return menu
