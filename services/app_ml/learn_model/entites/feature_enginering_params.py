import yaml
from typing import List
from pydantic import BaseModel, Field


class PolynomialFeaturesParams(BaseModel):
    poly_degree: int = Field(default=2)


class KBinsDiscretizerParams(BaseModel):
    kbins_n_bins: int = Field(default=5)


class SplineTransformerParams(BaseModel):
    spline_degree: int = Field(default=3)
    spline_k_nots: int = Field(default=3)


class AutoFeatParams(BaseModel):
    feateng_steps: int = Field(default=2)
    max_gb: int = Field(default=2)
    transformations: List[str] = Field(default=['1/', 'log', 'abs', 'sqrt'])
    n_jobs: int = Field(default=1)


class FeatureEngineeringParams(BaseModel):
    polynomial: PolynomialFeaturesParams
    kbins_discretizer: KBinsDiscretizerParams
    spline: SplineTransformerParams
    autofeat: AutoFeatParams


def get_feature_engineering_params(path: str) -> FeatureEngineeringParams:
    with open(path, 'r') as input_data:
        config_params = yaml.safe_load(input_data)
        return FeatureEngineeringParams(
            polynomial=PolynomialFeaturesParams(
                **config_params['PolynomialFeatures']),
            kbins_discretizer=KBinsDiscretizerParams(
                **config_params['KBinsDiscretizer']),
            spline=SplineTransformerParams(
                **config_params['SplineTransformer']),
            autofeat=AutoFeatParams(**config_params['AutoFeat'])
        )
