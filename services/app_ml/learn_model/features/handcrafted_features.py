import logging
import pandas as pd
from geopy.distance import geodesic


logger = logging.getLogger(__name__)


class HandCraftFeatures:

    def __init__(self):
        self.center_coords = (59.932464, 30.349258)
        self.year = 2024

    def calculate_distance(self, row: pd.Series) -> float:
        """Расчет километража от объекта до центра Питера"""
        point_coords = (row['latitude'], row['longitude'])
        return geodesic(point_coords, self.center_coords).kilometers

    def create_feature(self, df: pd.DataFrame) -> pd.DataFrame:
        df['house_age'] = self.year - df['build_year']
        df['distance_to_center'] = df.apply(self.calculate_distance, axis=1)
        df = df.drop(['build_year', 'latitude', 'longitude'], axis=1)
        logger.info(msg='Ручные признаки созданы')
        return df
