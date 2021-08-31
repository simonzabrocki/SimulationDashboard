from ggmodel_dev.models.utils import all_model_dictionary, all_model_properties_df

def render_model_dictionnary(model_dict, path):

    for model_name, model in model_dict.items():
        save_path = f'{path}/{model_name}_graph'
        print(model_name, save_path)
        graph_draw = model.draw()
        graph_draw.render(save_path)

if __name__ == '__main__':
    render_model_dictionnary(all_model_dictionary, 'outputs')
