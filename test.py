import pandas as pd
import yaml
from learn_model.data.get_dataset import get_data
from learn_model.entites.model_params import get_train_params
from learn_model.entites.feature_enginering_params import get_feature_engineering_params
from learn_model.features.build_features import Transformer
from learn_model.entites.model_params import FeatureParams
from learn_model.features.handcrafted_features import HandCraftFeatures
from learn_model.fit_model.fit_pipeline import train_model_pipeline
# data = pd.read_csv('/home/mle-user/mle-project-sprint-3-v001/data/dataset.csv')
# print(data.dtypes)


# params = get_train_params("/home/mle-user/mle-project-sprint-3-v001/config/config_decision_tree.yaml")
# train_df, test_df = get_data(params.data)

# train_df = HandCraftFeatures().create_feature(train_df)
# train_df = train_df.drop(['id', 'id_build_flat'], axis=1)

# test_df = HandCraftFeatures().create_feature(test_df)
# test_df = test_df.drop(['id', 'id_build_flat'], axis=1)

# print(train_df.shape)
# print(test_df.shape)


# print(train_df.columns)

# transform = Transformer(params.features)
# transform.fit(train_df.drop(['price'], axis=1), train_df['price'])
# data = transform.transform(test_df)
# print(data)
# print(data.shape)
# print()
# print(transform.get_feature_names_out)
# data.to_csv('test.csv')

train_model_pipeline("/home/mle-user/mle-project-sprint-3-v001/config/config_decision_tree.yaml")

# with open("/home/mle-user/mle-project-sprint-3-v001/config/config_decision_tree.yaml", "r") as input_data:
#     config_params = yaml.safe_load(input_data)

# print(config_params['model']['metric_path'])