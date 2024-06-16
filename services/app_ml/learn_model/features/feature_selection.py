import logging

import pandas as pd

from mlxtend.feature_selection import SequentialFeatureSelector



logger = logging.getLogger(__name__)


class FeatureSelection:

    def __init__(self, model, X_train, y_train):
        self.k_sfs_features = 10
        self.model = model
        self.X_train = X_train
        self.y_train = y_train

    def selection(self) -> tuple:
        sfs = SequentialFeatureSelector(self.model,
                                        k_features=self.k_sfs_features,
                                        forward=True,
                                        floating=False,
                                        scoring='r2',
                                        cv=2,
                                        n_jobs=-1)

        logger.info(msg="Отбор признаков начался")
        sfs.fit(self.X_train, self.y_train)
        logger.info(msg="Отбор признаков окончен")

        selected_feature_sfs = sfs.k_feature_idx_

        return selected_feature_sfs
