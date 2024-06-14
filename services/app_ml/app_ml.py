import logging

from fastapi import FastAPI, HTTPException
import uvicorn

from data_utils import InputData, OutputData
from fastapi_handler import FastApiHandler


logger = logging.getLogger(__name__)

app = FastAPI()
handler = None

# Функция, срабатывающая при запуске сервера


@app.on_event("startup")
def startup():
    try:
        global handler
        handler = FastApiHandler(model_path='/home/mle-user/mle-project-sprint-3-v001/models/model.pkl',
                                 transform_path='/home/mle-user/mle-project-sprint-3-v001/models/transformer.pkl',
                                 best_feature_path='/home/mle-user/mle-project-sprint-3-v001/models/best_features.txt')
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
