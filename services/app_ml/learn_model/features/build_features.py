import logging
import pandas as pd
import numpy as np
import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (KBinsDiscretizer, OneHotEncoder,
                                   PolynomialFeatures, SplineTransformer,
                                   StandardScaler)
from autofeat import AutoFeatRegressor
from category_encoders import CatBoostEncoder

from app_ml.learn_model.preprocess_params.model_params import FeatureParams
from app_ml.learn_model.preprocess_params.feature_enginering_params import get_feature_engineering_params

PATH_BASE_DIR = os.path.dirname(os.path.abspath(__name__))
PATH_YAML_FE = os.path.join(PATH_BASE_DIR, 'app_ml/config', 'config_feature_engineering.yaml')

logger = logging.Logger(__name__)

# переопределили класс transformer


class AutoFeatWrapper(BaseEstimator, TransformerMixin):
    def __init__(self, feateng_cols, feateng_steps=2, max_gb=2, transformations=['1/', 'log', 'abs', 'sqrt'], n_jobs=1):
        self.feateng_cols = feateng_cols
        self.feateng_steps = feateng_steps
        self.max_gb = max_gb
        self.transformations = transformations
        self.n_jobs = n_jobs
        self.afc = AutoFeatRegressor(feateng_cols=self.feateng_cols,
                                     feateng_steps=self.feateng_steps,
                                     max_gb=self.max_gb,
                                     transformations=self.transformations,
                                     n_jobs=self.n_jobs)

    def fit(self, X, y=None):
        self.afc.fit(X, y)
        return self

    def transform(self, X):
        return self.afc.transform(X)

    def get_feature_names_out(self, input_features=None):
        # Преобразуем данные и возвращаем имена фичей из DataFrame
        transformed_X = self.afc.transform(pd.DataFrame(
            np.zeros((1, len(self.feateng_cols))), columns=self.feateng_cols))
        return transformed_X.columns.tolist()


class Transformer(BaseEstimator, TransformerMixin):

    def __init__(self, features: FeatureParams):

        self.feature_for_autofeat = ['kitchen_area',
                                     'living_area',
                                     'total_area',
                                     'house_age',
                                     'ceiling_height']

        self.feature_for_kbins_transformer = ['house_age',
                                              'ceiling_height']

        self.feature_for_poly_spline_transformer = ['kitchen_area',
                                                    'living_area',
                                                    'total_area',
                                                    'ceiling_height']

        self.feature_for_OHE = ['is_apartment', 'has_elevator']
        self.feature_for_target_encoding = ['building_type_int', 'rooms']
        self.feature_tail_scaler = ['flats_count',
                                    'floors_total',
                                    'floor',
                                    'distance_to_center']

        self.target = ['price']
        self.features = features.features
        self.target = features.target
        self.FE_params = get_feature_engineering_params(PATH_YAML_FE)

        self.poly_transformer = PolynomialFeatures(
            degree=self.FE_params.polynomial.poly_degree,
            include_bias=False
        )
        self.kbins_transformer = KBinsDiscretizer(
            n_bins=self.FE_params.kbins_discretizer.kbins_n_bins,
            encode='ordinal',
            strategy='uniform'
        )
        self.spline_transformer = SplineTransformer(
            n_knots=self.FE_params.spline.spline_k_nots,
            degree=self.FE_params.spline.spline_degree
        )

        self.afc = AutoFeatRegressor(feateng_cols=self.feature_for_autofeat,
                                     feateng_steps=self.FE_params.autofeat.feateng_steps,
                                     max_gb=self.FE_params.autofeat.max_gb,
                                     transformations=self.FE_params.autofeat.transformations,
                                     n_jobs=self.FE_params.autofeat.n_jobs)

        self.catboost_category_encoder = CatBoostEncoder(return_df=False)
        self.ohe_encoder = OneHotEncoder(drop='if_binary')

    def fill_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Заполняет пропуски в числовых столбцах средним значением,
        а в категориальных столбцах значением 'unknown'.

        :param df: Исходный DataFrame
        :return: DataFrame с заполненными пропусками
        """
        # Обрабатываем числовые столбцы
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            mean_value = df[col].mean()
            df[col] = df[col].fillna(mean_value)

        # Обрабатываем категориальные столбцы
        categorical_columns = df.select_dtypes(
            include=[object, 'category']).columns
        for col in categorical_columns:
            df[col] = df[col].fillna('unknown')

        return df

    def pipe(self):
        poly_scaler_pipeline = Pipeline(steps=[
            ('poly_spline_auto', self.poly_transformer),
            ('scaler', StandardScaler())
        ])

        spline_scaler_pipeline = Pipeline(steps=[
            ('spline_spline_auto', self.spline_transformer),
            ('scaler', StandardScaler())
        ])

        autofeat_scaler_pipeline = Pipeline(steps=[
            ('autofeat_spline_auto', AutoFeatWrapper(
                feateng_cols=self.feature_for_autofeat)),
            ('scaler', StandardScaler())
        ])

        tail_scaler_pipeline = Pipeline(steps=[
            ('tail_feature_scaler', StandardScaler())
        ])

        preprocessor = ColumnTransformer(transformers=[
            ('poly', poly_scaler_pipeline, self.feature_for_poly_spline_transformer),
            ('spline', spline_scaler_pipeline,
             self.feature_for_poly_spline_transformer),
            ('afc', autofeat_scaler_pipeline, self.feature_for_autofeat),
            ('tail_scaler', tail_scaler_pipeline, self.feature_tail_scaler),
            ('category_encoder', self.catboost_category_encoder,
             self.feature_for_target_encoding),
            ('ohe', self.ohe_encoder, self.feature_for_OHE),
            ('kbins', self.kbins_transformer,
             self.feature_for_kbins_transformer)
        ],  remainder='passthrough',
            verbose_feature_names_out=True)

        return preprocessor

    def fit(self, df: pd.DataFrame, target):
        df = self.fill_missing_values(df)
        self.preprocessor = self.pipe().fit(df, target)
        logger.info(msg='Трансформер обучен')
        return self.preprocessor

    def transform(self, df: pd.DataFrame, target=None):
        new_df = pd.DataFrame(self.preprocessor.transform(
            df), columns=self.preprocessor.get_feature_names_out())
        self.get_feature_names_out = new_df.columns
        logger.info(msg='Данные трансформированы')
        return new_df

    def get_feature_names_out(self, input_features=None):
        if self.get_feature_names_out is None:
            raise RuntimeError("Для начала обучите трансформер")
        return self.get_feature_names_out
