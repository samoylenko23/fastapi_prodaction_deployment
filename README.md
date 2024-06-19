# Разработка ML-сервиса на FastAPI с выкаткой в продакшн и мониторингом Prometheus и Grafana

Добро пожаловать в репозиторий демонстрации написания pipeline обучения модели, с Feature Engineering и отбором признаков, создание микросервиса на FastAPI для работы с ML, мониторинг ML моделей, выведенных в продакшн, а также контейнеризация написанного сервиса для работы в продакшн.

Разберем это на примере предсказания стоимости квартир для сервиса Яндекс Недвижимости.

В Instruction.md и Monitoring.md описаны процессы запуска всех сервисов проекта.

## Используемые инструменты и библиотеки
1. FastAPI
2. Docker
3. Prometheus
4. Grafana
5. Pydantic
6. Uvicorn
7. Scikit-learn
8. click
9. PostgreSQL
10. Mlxtend, AutoFeat

### Сделано
1. Написан модуль learn_model для переобучения новой модели с проверкой входящих типов данных, Feature Engineering и отбором признаков, понадобится при обновлении исторических данных, позволит быстро обновить модель.

Для переобучения модели нужно запустить:

```
python3 services/fit_pipeline.py
```


2. Написан FastAPI-микросервис для работы с ML-моделью.
3. Развернуты Prometheus и Grafana для мониторинга работы модели.
4. Написаны кастомные метрики для мониторинга модели в real-time.
5. Контейнеризация всех микросервисов выше.
6. Написан модуль валидации входных параметров в YAML-файлах, и входных данных в сервис ML c помощью Pydantic.
7. Создан дашборд для анализа модели в проде.


# Структура проекта
```
model_prodaction_deployment
├── data - данные для обучения
│  ├── data_loader.py - загрузка из витрины данных
│  └── dataset.csv
├── services
│  ├── app_ml
│  │  ├── config - конфиги обучения
│  │  │  ├── config_decision_tree.yaml
│  │  │  ├── config_feature_engineering.yaml
│  │  │  └── config_predict.yaml
│  │  ├── handler_ml
│  │  │  ├── __init__.py
│  │  │  └── fastapi_handler.py - класс-обработчик для ml
│  │  ├── learn_model - модуль обучения новой модели
│  │  │  ├── data
│  │  │  │  ├── __init__.py
│  │  │  │  └── get_dataset.py
│  │  │  ├── features - создание фичей и оборчивание в трансформеры для pipeline
│  │  │  │  ├── __init__.py
│  │  │  │  ├── build_features.py
│  │  │  │  ├── feature_selection.py
│  │  │  │  └── handcrafted_features.py
│  │  │  ├── preprocess_params - загрузка параметров с проверкой pydantic
│  │  │  │  ├── __init__.py
│  │  │  │  ├── feature_enginering_params.py
│  │  │  │  └── model_params.py
│  │  │  └── __init__.py
│  │  ├── models
│  │  │  ├── best_features.txt
│  │  │  ├── model.pkl
│  │  │  └── transformer.pkl
│  │  ├── utils - загрузка данных для приложения
│  │  │  └── data_utils.py
│  │  ├── __init__.py
│  │  └── app.py - приложение ml на FastAPI
│  ├── prometheus
│  │  └── prometheus.yml
│  ├── fit_pipeline.py - скрипт для переобучения модели
│  └── generate_requests.py - нагрузка для тестирования
├── .env
├── .gitignore
├── Dockerfile_ml_service
├── Instructions.md
├── Monitoring.md
├── README.md
├── docker-compose.yaml
├── image.png
├── monitoring_model_price.json
└── requirements.txt
```

Отмечу, что в модуле learn_model происходит переобучения модели для новых данных. Проверяем с помощью pydantic валидацию модели yaml. Загружаем данные и обрабатываем их в написанном трансформере, также указываем класс для обработки ручных признаков. Также в этом модуле происходит отбор признаков с помощью mlxtend, лучшие отобранные признаки используются для нового обучения модели и дальнейшего ее использования в сервисе ml.