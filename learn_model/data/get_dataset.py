import logging
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

from learn_model.entites.model_params import DatasetParams, SplittingParams

# возьмет имя модуля из атрибута __name__
logger = logging.getLogger(__name__)


def read_dataset(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        logger.info(msg='Датасет загружен')
    except IOError as e:
        logger.error(msg='Ошибка загрузки данных')
        raise e
    return df


def split_train_test_data(df: pd.DataFrame, splitting_params: SplittingParams) \
        -> Tuple[pd.DataFrame, pd.DataFrame]:
    logger.info(msg='Данные разбиты для обучения')

    return train_test_split(
        df,
        test_size=splitting_params.test_size,
        random_state=splitting_params.random_state
    )


def get_data(params: DatasetParams) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = read_dataset(params.data_path)
    return split_train_test_data(df, params.splitting_params)
