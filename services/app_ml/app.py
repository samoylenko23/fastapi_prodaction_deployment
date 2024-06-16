import logging
import os
from fastapi import FastAPI, HTTPException
import uvicorn

import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.data_utils import InputData, OutputData
from handler_ml.fastapi_handler import FastApiHandler


logger = logging.getLogger(__name__)

app = FastAPI()
handler = None


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Создаем пути к файлам моделей
model_path = os.path.join(BASE_DIR, 'models', 'model.pkl')
transform_path = os.path.join(BASE_DIR, 'models', 'transformer.pkl')
best_feature_path = os.path.join(BASE_DIR, 'models', 'best_features.txt')

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
        prediction = handler.handle(request.model_dump())
    except Exception as e:
        raise HTTPException(  # Если что-то идёт не так, выдаём ошибку и код 500
            status_code=500,
            detail=f"Error: something went wrong while prediction {e}")
    logger.info(msg="Предсказание выполнено успешно")
    return prediction


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
