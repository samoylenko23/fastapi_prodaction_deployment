import logging
import os
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram, Counter, Summary
import uvicorn

import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.data_utils import InputData, OutputData
from handler_ml.fastapi_handler import FastApiHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)

# Создаем пути к файлам моделей
model_path = os.path.join(BASE_DIR, 'models', 'model.pkl')
transform_path = os.path.join(BASE_DIR, 'models', 'transformer.pkl')
best_feature_path = os.path.join(BASE_DIR, 'models', 'best_features.txt')

# метрика для подсчета предсказаний больших 10 и 20 млн
main_app_bigger_prediction = Histogram(
    "main_app_bigger_prediction",
    "Histogram of bigger prediction anomaly",
    buckets=[1e7, 2e7]
)

# Создаем Summary для хранения предсказаний
prediction_summary = Summary('prediction_summary', 'Summary of predictions')

# Создаем Counter для учета ошибок
error_counter = Counter('error_counter', 'Count of errors')
handler = None


app = FastAPI()
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Функция, срабатывающая при запуске сервера
@app.on_event("startup")
def startup():
    try:
        global handler
        handler = FastApiHandler(model_path=model_path,
                         transform_path=transform_path,
                         best_feature_path=best_feature_path)
    except Exception as e:
        logger.error("Ошибка загрузки моделей")
        raise ImportError("Проверьте правильностей путей загрузки моделей")


# При открытии корневой страницы пишем, что всё хорошо
@app.get("/")
def main():
    return "Готов к предсказаниям :)"

# Функция, которая получает данные в post-запросе и возвращает предсказание
@app.post("/predict", response_model=OutputData)
def predict(request: InputData):
    try:
        logger.info(f"Received request data: {request.dict()}")
        prediction = handler.handle(request.dict())
        # Добавляем предсказание в Summary
        prediction_summary.observe(prediction.predicted_value)
        main_app_bigger_prediction.observe(prediction.predicted_value)
    except Exception as e:
        error_counter.inc()
        raise HTTPException(
            status_code=500,
            detail=f"Error: something went wrong while prediction {e}"
        )
    logger.info("Предсказание выполнено успешно")
    return prediction


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
