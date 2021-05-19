from ggmodel_dev.models.greengrowth import GGGM
import pandas as pd

model_group_df = pd.DataFrame({'model_group': ['Landuse', 'Water', 'Green Growth'],
                                'symbol': [ "🌾🌲", "💧", '🌱']})

all_model_properties_df = (
            pd.DataFrame.from_dict(GGGM.all_model_properties, orient='index')
            #.reset_index()
            #.rename(columns={'index': 'model'})
            .merge(model_group_df, on=['model_group'])
)


all_model_properties = GGGM.all_model_properties
all_model_dictionary = GGGM.all_model_dictionary