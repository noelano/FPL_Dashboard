import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

from microbiome_viewer.app import (
    app, abundances, meta, rel_abundances, metric_df, bacteria_of_concern, var_x, var_y, pal,
)


GENERA = [x for x in abundances.columns if x not in ['Sample']]
colour_options = {c: c for c in meta.columns if c != 'ID'}
checkbox_value = [1] if len(bacteria_of_concern) > 0 else None


layout = html.Div([

    html.Div([

        html.Div([

            html.Div([

                html.Div([
                    html.H6(
                        id='n_samples'
                    ),
                    html.P("Samples"),
                    ],
                    className='one column', id='metric',
                    style={'margin-left': 'auto', 'margin-right': 'auto', 'float': 'left', 'width': '33.3%'}
                ),

                html.Div([
                    html.H6(
                        id='n_bacteria'
                    ),
                    html.P("Distinct Bacteria"),
                    ],
                    className='one column', id='metric',
                    style={'margin-left': 'auto', 'margin-right': 'auto', 'float': 'left', 'width': '33.3%'}
                ),

                html.Div([
                    html.H6(
                        id='n_reads'
                    ),
                    html.P("Reads"),
                    ],
                    className='one column', id='metric',
                    style={'margin-left': 'auto', 'margin-right': 'auto', 'float': 'left', 'width': '33.3%'})

                ],
                className='row'
            ),

            html.Div([

                dcc.Checklist(
                    id='bacteria_selection',
                    options=[
                        {'label': 'Only bacteria of concern', 'value': 1}
                    ],
                    values=checkbox_value,
                    style={'display': 'inline' if len(bacteria_of_concern) > 0 else 'none'}
                ),

                dcc.Checklist(
                    id='relative_abundance',
                    options=[
                        {'label': 'Show relative abundances', 'value': 1}
                    ],
                    values=[1]
                ),

                html.P("Colour plots by:"),

                dcc.Dropdown(
                    id='colour_select',
                    options=[{'label': colour_options[i], 'value': i} for i in colour_options],
                    value=None,
                    clearable=True,
                ),

                html.P("Plot sample similarity using:"),

                dcc.RadioItems(
                    id='projection_selector',
                    options=[
                        {'label': 'Bray-Curtis', 'value': 'mds'},
                        {'label': 'Aitchison', 'value': 'aitchison'},
                        {'label': 'PCA', 'value': 'pca'},
                        {'label': 't-SNE', 'value': 'tsne'},
                    ],
                    value='mds',
                    labelStyle={'display': 'inline-block'}
                ),
                ],
                className='pretty_container'
            )
            ],
            className='six columns'
        ),

        html.Div([

            html.Div([

                dcc.Graph(id='microorganisms'),

                ],
                id='histContainer'
            ),
            ],
            className='six columns',
            style={'height': 350}
        ),

        ],
        className='row'
    ),

    html.Div([

        html.Div([

            dcc.Graph(
                id='beta',
                style={
                    # 'margin-top': 20,
                    'height': '40%',
                    # 'width': '75vh'
                },
            ),

            ],
            className='beta_container six columns'
        ),

        html.Div([

            dcc.Graph(id='microbiome', style={'height': '100%'})

            ],
            className='six columns'
        ),

    ], className='row'
    )

    ],
    className='twelve columns'
)


@app.callback(
    dash.dependencies.Output('n_samples', 'children'),
    [dash.dependencies.Input('beta', 'selectedData')]
)
def update_n_samples(samples):
    if samples:
        samples = [x["customdata"] for x in samples["points"]]
        dff = abundances[abundances['Sample'].isin(list(samples))]
    else:
        dff = abundances.copy()

    n_samples = dff.shape[0]

    return f"{n_samples:,}"


@app.callback(
    dash.dependencies.Output('n_bacteria', 'children'),
    [dash.dependencies.Input('beta', 'selectedData')]
)
def update_n_genera(samples):
    if samples:
        samples = [x["customdata"] for x in samples["points"]]
        dff = abundances[abundances['Sample'].isin(list(samples))]
    else:
        dff = abundances.copy()

    dff = dff.drop('Sample', axis=1)
    n_genera = dff.loc[:, (dff != 0).any(axis=0)].shape[1]

    return f"{n_genera:,}"


@app.callback(
    dash.dependencies.Output('n_reads', 'children'),
    [dash.dependencies.Input('beta', 'selectedData')]
)
def update_n_reads(samples):
    if samples:
        samples = [x["customdata"] for x in samples["points"]]
        dff = abundances[abundances['Sample'].isin(list(samples))]
    else:
        dff = abundances.copy()

    dff = dff.drop('Sample', axis=1)
    n_reads = int(dff.values.sum())

    text = f"{n_reads:,}"

    return text


@app.callback(
    dash.dependencies.Output('beta', 'figure'),
    [dash.dependencies.Input('projection_selector', 'value'),
     dash.dependencies.Input('colour_select', 'value')]
)
def update_beta(projection_selector, colour_select):
    dff = metric_df.merge(meta, left_on='Sample', right_on='ID')
    dff.drop('ID', axis=1, inplace=True)

    if colour_select is None:
        data = [
                {
                    'x': dff[f'{projection_selector}_x'],
                    'y': dff[f'{projection_selector}_y'],
                    'mode': 'markers',
                    'text': dff['Sample'],
                    'hoverinfo': "text",
                    'customdata': dff['Sample'],
                    'opacity': 0.8,
                    'marker': {
                        'size': 10,
                        'line': {
                            'color': 'gray',
                            'width': 1,
                        },
                    },
                }
            ]
    else:
        data = [
                {
                    'x': dff[dff[colour_select] == c][f'{projection_selector}_x'],
                    'y': dff[dff[colour_select] == c][f'{projection_selector}_y'],
                    'name': c,
                    'mode': 'markers',
                    'text': dff[dff[colour_select] == c]['Sample'],
                    'hoverinfo': "text",
                    'customdata': dff[dff[colour_select] == c]['Sample'],
                    'opacity': 0.8,
                    'marker': {
                        'size': 10,
                        'line': {
                            'color': 'gray',
                            'width': 1,
                        },
                    },
                } for c in dff[colour_select].unique()
            ]

    return {
            'data': data,
            'layout': {
                'title': 'Beta Diversity of Samples',
                'hovermode': 'closest',
                'xaxis': {
                    'showgrid': False,
                    'zeroline': False,
                    'showline': True,
                    'ticks': '',
                    'showticklabels': False,
                    'title': f"Component 1. Variance {var_x:.2f}%" if projection_selector == 'pca' else ""
                },
                'yaxis': {
                    'showgrid': False,
                    'zeroline': False,
                    'showline': True,
                    'ticks': '',
                    'showticklabels': False,
                    'title': f"Component 2. Variance {var_y:.2f}%" if projection_selector == 'pca' else ""
                },
                'dragmode': 'select',
                'autosize': True,
                # 'height': 600,
                # 'width': 600
            }
        }


@app.callback(
    dash.dependencies.Output('microorganisms', 'figure'),
    [dash.dependencies.Input('bacteria_selection', 'values'),
     dash.dependencies.Input('beta', 'selectedData')]
)
def update_histo(bacteria, samples):
    # Filter to selection
    if samples:
        samples = [x["customdata"] for x in samples["points"]]
        dff = abundances[abundances['Sample'].isin(list(samples))]
    else:
        dff = abundances.copy()

    # Drop Sample as its no longer needed
    dff.drop('Sample', axis=1, inplace=True)
    total = dff.values.sum()

    if bacteria:
        genus_list = [c for c in abundances.columns if c in bacteria_of_concern]
        genus_list.sort()
        dff = dff[genus_list]

    # Get counts of hazard categories and convert to proportions
    counts = dff.sum(axis=0)
    counts *= (100.0 / total)
    counts.sort_values(ascending=False, inplace=True)

    counts = counts.head(20)

    return {
            'data': [
                go.Bar(
                    x=counts.index,
                    y=counts.values
                )
            ],
            'layout': {
                'title': 'Top microorganisms by relative abundance',
                'hovermode': 'closest',
                'autosize': True,
                'automargin': True,
                'yaxis': {
                    'title': 'Relative Abundance (%)'
                }
            }
    }


@app.callback(
    dash.dependencies.Output('microbiome', 'figure'),
    [dash.dependencies.Input('bacteria_selection', 'values'),
     dash.dependencies.Input('relative_abundance', 'values'),
     dash.dependencies.Input('beta', 'selectedData')]
)
def update_stacks(bacteria, show_relative, samples):
    if len(show_relative) > 0:
        dff = rel_abundances.copy()
    else:
        dff = abundances.copy()

    # Filter to selection
    if samples:
        samples = [x["customdata"] for x in samples["points"]]
        dff = dff[dff['Sample'].isin(list(samples))]

    # Sort columns alphabetically
    dff.sort_index(axis=1, inplace=True)

    if bacteria:
        genus_list = [c for c in abundances.columns if c in bacteria_of_concern]
        genus_list.sort()
        dff['Total'] = dff.drop(['Sample'], axis=1).sum(axis=1)
        dff['Others'] = dff['Total'] - dff[genus_list].sum(axis=1)
        dff = dff[['Sample'] + genus_list + ['Others']]

    to_drop = [x for x in ['Sample'] if x in dff.columns]
    genera = dff.drop(to_drop, axis=1).columns

    data = []

    ind = 0
    for genus in genera:
        counts = dff[genus].values
        trace = go.Bar(
                    y=counts,
                    x=dff['Sample'].values,
                    name=genus,
                    # orientation='h',
                    marker=dict(
                        color=pal[ind % 20],
                    )
                )
        data.append(trace)
        ind += 1

    return {
        'data': data,
        'layout': go.Layout(
            barmode='stack',
            hovermode='closest',
            title='Microorganisms per sample',
            showlegend=True if bacteria else False
        )
    }

