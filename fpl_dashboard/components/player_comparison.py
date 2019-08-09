import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

from fpl_dashboard import S3_URL
from fpl_dashboard.app import players, history, fixtures, max_stats, app


# Assign labels to the main stats of interest
COMMON_STATS = {
    'total_points': 'Total Points',
    'now_cost': 'Current Cost',
    'bonus': 'Total Bonus Points',
    'points_per_game': 'Points per Game',
}

player_list = players[['full_name', 'id']].rename(
    {'full_name': 'label', 'id': 'value'}, axis=1
).to_dict('records')

layout = html.Div([

    html.Div([

        dcc.Dropdown(
            id='player_select_1',
            options=player_list,
            value=None,
            clearable=True,
            placeholder='Select a player'
        ),

        html.Div(id='player1')

        ],
        className='six columns'
    ),

    html.Div([

        dcc.Dropdown(
            id='player_select_2',
            options=player_list,
            value=None,
            clearable=True,
            placeholder='Select a player'
        ),

        html.Div(id='player2')

        ],
        className='six columns'
    ),

    ],
    className='twelve columns'
)


def return_player_stats(player_id):
    div_contents = []

    if player_id:
        # Filter dataframes
        player = players[players['id'] == player_id].iloc[0]
        player_hist = history[history['player_id'] == player_id]
        player_fixt = fixtures[fixtures['player_id'] == player_id]

        # Add generic outputs
        img_url = S3_URL + 'p' + player['photo'].replace('jpg', 'png')
        div_contents.append(html.Img(src=img_url))
        div_contents += common_stats(player)

        # Depending on the position, specific content will be added:
        position = player['element_type']
        if position == 1:
            div_contents.append(goalkeeper_view(player))
        elif position == 2:
            div_contents.append(defender_view(player))
        elif position == 3:
            div_contents.append(midfielder_view(player))
        elif position == 4:
            div_contents.append(striker_view(player))

        # Add next few fixtures
        # TODO

        # Add form
        # TODO

    return div_contents


def stat_row_helper(label, value, max_value):
    return html.Div([
        html.Div([
            label
        ], className='two columns'),

        html.Div([
            dcc.Graph(
                figure={
                    'data': [go.Bar(x=[value], y=[1], orientation='h')],
                    'layout': {
                        'xaxis': {
                            'domain': [0, max_value],
                            'showgrid': False,
                            'zeroline': False,
                            'showline': False,
                            'ticks': '',
                            'showticklabels': False,
                        },
                        'yaxis': {
                            'showgrid': False,
                            'zeroline': False,
                            'showline': False,
                            'ticks': '',
                            'showticklabels': False,
                        },
                        'height': 80,
                        'margin': {
                            'l': 0,
                            'r': 0,
                            'b': 0,
                            't': 0,
                        },
                    }
                }
            )
        ], className='three columns', style={'height': 100}),
    ], className='row')


def common_stats(player_stats):
    return [stat_row_helper(COMMON_STATS[stat], player_stats[stat], max_stats[stat]) for stat in COMMON_STATS]


def defender_view(player_stats):
    pass


def goalkeeper_view(player_stats):
    pass


def striker_view(player_stats):
    pass


def midfielder_view(player_stats):
    pass


@app.callback(
    dash.dependencies.Output('player1', 'children'),
    [dash.dependencies.Input('player_select_1', 'value')]
)
def update_player1(player_id):
    return return_player_stats(player_id)


@app.callback(
    dash.dependencies.Output('player2', 'children'),
    [dash.dependencies.Input('player_select_2', 'value')]
)
def update_player2(player_id):
    return return_player_stats(player_id)
