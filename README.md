# Привет! Спасибо за проверку!)

# Ответы на змечания

1. 2024 год не дает ввести, так как ограничил это в pydantic)
2. Моменты с проблемой запусков контейнеров поправил. Также вернул файл .env из gitignore, чтобы лежал в репозитории. Ранее я его в instrictions.md описывал, но лучше сохраню его файлом, чтобы сборки проходили сразу и людям не нужно было его создавать. Ничего секретного там сейчас не храню)
3. По файлу monitoring.md - согласен, гистограмма для 10 млн модно убрать, большая часть значений будет больше) но просто нет времени перестраивать дашборд и скрины, учту этот момент на будущее
4. Файл fit_pipeline.py для обучения новой модели вынес специально в корень проекта, чтобы пользователю было удобно с корня запустить сразу и процесс обновления датасета и переобучение новой модели. По поводу того, что мы обучение делали в прошлом уроке - да, но там мы в тетрадках были, а тут попытался выбраться в боевые условия. В реальности ведь так и происходит, что модель учат в итоге так как сделал я? ПОделись, пожалуйста, свои опытом, как этот процесс устроен у тебя
5. По поводу файла generate_requests.py, ты просто не заметила, что я прибавлял к некоторым значениям словаря +i , поэтому запрос был точно каждый раз разный) Сейчас, чтобы было лучше заметно - начал отправлять рандомное число)
6. Можешь, пожалуйста, дать какие-то рекомендации по моему коду?


# Разработка ML-сервиса с выкаткой в продакшн и мониторигом системы

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
python3 fit_pipeline.py
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
├── data -> данные для обучения
│  └── dataset.csv
├── models 
│  ├── best_features.txt -> индексы лучших отобранных признаков
│  ├── model.pkl -> обученная модель
│  └── transformer.pkl -> обученный трансформер
├── services
│  ├── app_ml -> микросервис с ML на FastAPI
│  │  ├── config -> файлы конфигурации
│  │  │  ├── config_decision_tree.yaml
│  │  │  ├── config_feature_engineering.yaml
│  │  │  └── config_predict.yaml
│  │  ├── handler_ml -> класс обработчик для ML сервиса
│  │  │  ├── __init__.py
│  │  │  └── fastapi_handler.py
│  │  ├── learn_model -> модуль для обучения новой модели
│  │  │  ├── data -> получение датасета по путям из YAML
│  │  │  │  ├── __init__.py
│  │  │  │  └── get_dataset.py
│  │  │  ├── entites -> извлечение сущностей из yaml
│  │  │  │  ├── __init__.py
│  │  │  │  ├── feature_enginering_params.py
│  │  │  │  └── model_params.py
│  │  │  ├── features -> создание собственного трансформера, ручная обработка и отбор признаков
│  │  │  │  ├── __init__.py
│  │  │  │  ├── build_features.py
│  │  │  │  ├── feature_selection.py
│  │  │  │  └── handcrafted_features.py
│  │  │  └── __init__.py
│  │  ├── models
│  │  │  ├── best_features.txt
│  │  │  ├── model.pkl
│  │  │  └── transformer.pkl
│  │  ├── utils
│  │  │  ├── __init__.py
│  │  │  └── data_utils.py -> валидация входящих и выходящих данных в FatAPI c помощью Pydantic
│  │  ├── __init__.py
│  │  └── app.py
│  └── prometheus
│     └── prometheus.yml -> настройки отслеживания метрик 
├── Dockerfile_ml_service -> запуск микросервиса просто из докера
├── Instructions.md
├── Monitoring.md
├── README.md
├── data_loader.py -> загрузка данных из витрины данных, понадобится для обновления исторических данных
├── docker-compose.yaml -> общий файл со всеми микросервисами
├── fit_pipeline.py -> файл для запуска обучения новой модели
├── generate_requests.py -> генерация запросов к сервису для тестирования монтиторинга
├── monitoring_model_price.json -> сохраненный дашборд Grafana
└── requirements.txt
```

Отмечу, что в модуле learn_model происходит переобучения модели для новых данных. Проверяем с помощью pydantic валидацию модели yaml. Загружаем данные и обрабатываем их в написанном трансформере, также указываем класс для обработки ручных признаков. Также в этом модуле происходит отбор признаков с помощью mlxtend, лучшие отобранные признаки используются для нового обучения модели и дальнейшего ее использования в сервисе ml.