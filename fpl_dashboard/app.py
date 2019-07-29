import dash
import seaborn as sns

from fpl_dashboard.api import load_all_data


# Load summary datasets from the API
teams, players, history, fixtures = load_all_data()

# set the palette
pal = sns.color_palette('tab20').as_hex()

# Serve the dash app
external_stylesheets = ['https://cdn.rawgit.com/plotly/dash-app-stylesheets/' +
                        '2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
