import logging
import click
import os
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score

from learn_model.data.get_dataset import get_data
from learn_model.entites.model_params import get_train_params
from learn_model.features.handcrafted_features import HandCraftFeatures
from learn_model.features.build_features import Transformer
from learn_model.features.feature_selection import FeatureSelection

PATH_ARTIFACT = "/home/mle-user/mle-project-sprint-3-v001/models"
logger = logging.getLogger(__name__)


def train_model_pipeline(config_path):
    logger.info(msg='Старт обучения')

    params = get_train_params(config_path)
    train_df, test_df = get_data(params.data)
    logger.info(msg='Данные получены')

    train_df = HandCraftFeatures().create_feature(train_df)
    train_df = train_df.drop(['id', 'id_build_flat'], axis=1)

    test_df = HandCraftFeatures().create_feature(test_df)
    test_df = test_df.drop(['id', 'id_build_flat'], axis=1)

    transformer = Transformer(params.features)
    transformer.fit(train_df.drop(['price'], axis=1), train_df['price'])

    y_train = train_df['price']
    y_test = test_df['price']

    X_train = transformer.transform(train_df.drop(['price'], axis=1))
    X_test = transformer.transform(test_df.drop(['price'], axis=1))

    model = DecisionTreeRegressor(
        max_depth=params.model.model_params.max_depth,
        min_samples_leaf=params.model.model_params.min_samples_leaf,
        min_samples_split=params.model.model_params.min_samples_split,
        criterion=params.model.model_params.criterion,
    )

    best_features = FeatureSelection(model, X_train, y_train).selection()

    X_train = X_train.iloc[:, list(best_features)]
    X_test = X_test.iloc[:, list(best_features)]

    model.fit(X_train, y_train)
    logger.info(msg='Модель обучена')

    # Создаем директорию, если она не существует
    os.makedirs(PATH_ARTIFACT, exist_ok=True)   

        # Сохранение best_features в текстовый файл
    best_features_path = os.path.join(PATH_ARTIFACT, 'best_features.txt')
    with open(best_features_path, 'w') as f:
        for feature in best_features:
            f.write(f"{feature}\n")

    # Сохранение обученного трансформера
    transformer_path = os.path.join(PATH_ARTIFACT, 'transformer.pkl')
    joblib.dump(transformer, transformer_path)

    # Сохранение обученной модели
    model_path = os.path.join(PATH_ARTIFACT, 'model.pkl')
    joblib.dump(model, model_path)

    logger.info(msg='Модель, лучшие фичи и трансформер сохранены')


@click.command()
@click.option(
    "--config",
    required=True,
    type=str
)

def main(config):
    train_model_pipeline(config)

if __name__ == "__main__":
    main()