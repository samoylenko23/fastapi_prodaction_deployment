import logging
import os
import sys
from collections import OrderedDict

# Добавляем корневой каталог в sys.path
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../')))
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from fastapi import HTTPException
from pydantic import ValidationError

from data_utils import (
    get_best_features,
    get_model,
    get_transform,
    InputData,
    OutputData
)
from learn_model.features.handcrafted_features import HandCraftFeatures



class FastApiHandler:

    def __init__(self, model_path, transform_path,
                 best_feature_path):
        self.model = get_model(model_path)
        self.transform = get_transform(transform_path)
        self.best_features_idx = get_best_features(best_feature_path)
        self.hand_craft_feature = HandCraftFeatures()

    def predict(self, data: dict) -> float:

        ordered_params = ['building_type_int', 'latitude',
                          'longitude', 'ceiling_height',
                          'flats_count', 'floors_total',
                          'has_elevator', 'floor',
                          'kitchen_area', 'living_area',
                          'rooms', 'is_apartment',
                          'total_area', 'build_year']

        # в зависимости от версии питона, словарь может возвращать ключи в разном порядке
        # поэтому упорядочим словарь в нужном для модели виде
        data_ordered = OrderedDict((key, data[key]) for key in ordered_params)
        data = pd.DataFrame([data_ordered])
        logger.info("Данные получены")
        data = self.hand_craft_feature.create_feature(data)
        print(data)
        X_data = self.transform.transform(data)
        logger.info("Данные трансформированы")
        X_data_with_best_feature = X_data.iloc[:, list(self.best_features_idx)]
        logger.info("Выбраны лучшие признаки")
        # избавляемся от логарифмированного таргета
        return np.round(np.exp(self.model.predict(X_data_with_best_feature)), 2)[0]

    def handle(self, data: dict) -> OutputData:
        try:
            validated_data = InputData(**data)
            print(validated_data)
            prediction = self.predict(validated_data.model_dump())
            return OutputData(predicted_value=prediction)
        except ValidationError as e:
            raise HTTPException(status_code=400,
                                detail=str(e))
        except Exception as e:
            raise Exception(f"Problem with request: {str(e)}")


if __name__ == "__main__":

    # создаём тестовый запрос
    test_params = {
        "building_type_int": 6,
        "latitude": 55.71711349487305,
        "longitude": 37.78112030029297,
        "ceiling_height": 2.640000104904175,
        "flats_count": 84,
        "floors_total": 12,
        "has_elevator": True,
        "floor": 9,
        "kitchen_area": 9.899999618530272,
        "living_area": 19.899999618530277,
        "rooms": 1,
        "is_apartment": False,
        "total_area": 35.099998474121094,
        "build_year": 1965
    }

    # создаём обработчик запросов для API
    handler = FastApiHandler(model_path='/home/mle-user/mle-project-sprint-3-v001/models/model.pkl',
                             transform_path='/home/mle-user/mle-project-sprint-3-v001/models/transformer.pkl',
                             best_feature_path='/home/mle-user/mle-project-sprint-3-v001/models/best_features.txt')

    response = handler.handle(test_params)
    print(f"Ответ: {response}")
