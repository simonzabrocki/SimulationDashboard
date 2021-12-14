import dash
from data_utils import load_all_data


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True,

)

app.title = 'GreenBlueIndex'

server = app.server

INDEX_YEAR = 2020
MIN_YEAR = 2015

data, indicator_data, indicator_properties, dimension_properties, ISO_options, missing_data = load_all_data(max_year=INDEX_YEAR)