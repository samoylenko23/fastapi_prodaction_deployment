from typing import List, Optional
import yaml
from pydantic import BaseModel, Field



class SplittingParams(BaseModel):
    test_size: float = Field(default=0.3)
    random_state: int = Field(default=42)


class DatasetParams(BaseModel):
    data_path: str
    splitting_params: SplittingParams


class FeatureParams(BaseModel):
    features: List[str]
    target: Optional[str]


class DecisionTreeParams(BaseModel):
    max_depth: int = Field(default=9)
    min_samples_leaf: int = Field(default=2)
    min_samples_split: int = Field(default=3)
    criterion: str = Field(default='squared_error')


class ModelParams(BaseModel):
    save_path: str
    metric_path: str
    model: str = Field(default="DecisionTree")
    model_params: DecisionTreeParams


class TrainingParams(BaseModel):
    data: DatasetParams
    features: FeatureParams
    model: ModelParams


class PredictParams(BaseModel):
    model: str
    data_path: str
    result_path: str


def get_train_params(path: str) -> TrainingParams:
    with open(path, "r") as input_data:
        config_params = yaml.safe_load(input_data)
        return TrainingParams(
            data=DatasetParams(**config_params['data']),
            features=FeatureParams(**config_params['features']),
            model=ModelParams(
                save_path=config_params['model']['save_path'],
                metric_path=config_params['model']['metric_path'],
                model=config_params['model']['model'],
                model_params=DecisionTreeParams(
                    **config_params['model']['model_params'])
            )
        )


def get_predict_params(path: str) -> PredictParams:
    with open(path, "r") as input_data:
        config_params = yaml.safe_load(input_data)
        return PredictParams(
            model=config_params['model'],
            data_path=config_params['data_path'],
            result_path=config_params['result_path']
        )
