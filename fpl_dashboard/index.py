import dash
import dash_core_components as dcc
import dash_html_components as html

from fpl_dashboard.components import (
    player_comparison, header
)
from fpl_dashboard.app import app


# Define app layout
app.layout = html.Div([
    header.header(),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
], className='twelve columns')


# Callback to map urls to different layouts
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/fpl-dashboard/summary' or pathname == '/':
        return player_comparison.layout
    elif pathname == '/fpl-dashboard/player_compare':
        return player_comparison.layout
    else:
        return player_comparison.layout


if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
