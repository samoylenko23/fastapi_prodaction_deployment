from typing import Union, Dict
import joblib

from pydantic import BaseModel, Field
import pandas as pd


class InputData(BaseModel):
    """Описание модели входящих данных в запросе"""

    building_type_int: int = Field(default=6)
    latitude: float = Field(default=55.71711349487305)
    longitude: float = Field(default=37.78112030029297)
    ceiling_height: float = Field(
        default=2.640000104904175, description="Высота потолка", gt=1, lt=1e2)
    flats_count: int = Field(
        default=100, description="Количество квартир", gt=1, lt=2000)
    floors_total: int = Field(
        default=15, description="Общее количество этажей", gt=1, lt=100)
    has_elevator: bool = Field(default=True, description="Наличие лифта")
    floor: int = Field(default=12, description="Этаж", gt=1, lt=100)
    kitchen_area: float = Field(default=119.899999, description="Площадь кухни")
    living_area: float = Field(default=200.899999, description="Жилая площадь")
    rooms: int = Field(
        default=1, description="Количество комнат", gt=0, lt=1e2)
    is_apartment: bool = Field(
        default=True, description="Является ли квартира апартаментами")
    total_area: float = Field(
        default=39.099998, description="Общая площадь", gt=1, lt=1e4)
    build_year: int = Field(
        default=2000, description="Год постройки", gt=1800, lt=2030)

    @staticmethod
    def check_feature_names(data: Dict[str, Union[float, int, str]]):

        required_features = {'building_type_int',
                             'latitude',
                             'longitude',
                             'ceiling_height',
                             'flats_count',
                             'floors_total',
                             'has_elevator',
                             'floor',
                             'kitchen_area',
                             'living_area',
                             'rooms',
                             'is_apartment',
                             'total_area',
                             'build_year'}

        # проверка наличия всех обязательных фичей
        missing_features = required_features - data.keys()
        if missing_features:
            raise ValueError("Отсутствуют обязательные признаки")

        # Проверка на наличие недопустимых признаков
        if not set(data.keys()).issubset(required_features):
            raise ValueError('Неправильные имена признаков')

        # Валидация данных с помощью Pydantic
        try:
            validated_data = InputData(**data)
        except Exception as e:
            raise ValueError(f"Ошибка валидации данных: {e}")

        return validated_data


class OutputData(BaseModel):
    """Описание модели выходящих данных после запроса"""
    predicted_value: float


def get_model(path: str):
    model = joblib.load(path)
    return model


def get_transform(path: str):
    transform = joblib.load(path)
    return transform


def get_best_features(path: str) -> list:
    with open(path, 'r') as f:
        best_features = [int(line.strip()) for line in f]
    return best_features
