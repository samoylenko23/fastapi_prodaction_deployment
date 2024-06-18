# Инструкции по запуску микросервиса

Содержание .env для настройки сервисов:

```
AUTHOR="ALEXEY"
PORT_DOCKER_ML=8081
PORT_GRAFANA=3000
GRAFANA_USER="admin"
GRAFANA_PASSWORD="admin"
PROMETHEUS_PORT=9090
```

### 1. FastAPI микросервис в виртуальном окружение

Настройка виртуального окружения
```
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

Для запуска FastAPI микросервиса в виртуальном окружении необходимо запустить скрипт app.py:

```
python3 services/app_ml/app.py
```

Запустится unicorn. Для тестирования работы приложения откройте новый терминал и отправьте тестовый запрос через curl:

```
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{
    "building_type_int": 6,
    "latitude": 55.71711349487305,
    "longitude": 37.78112030029297,
    "ceiling_height": 2.640000104904175,
    "flats_count": 84,
    "floors_total": 12,
    "has_elevator": true,
    "floor": 9,
    "kitchen_area": 9.899999618530272,
    "living_area": 19.899999618530277,
    "rooms": 1,
    "is_apartment": false,
    "total_area": 35.099998474121094,
    "build_year": 1965
}'
```


### 2. FastAPI микросервис в Docker-контейнере

**Для запуска FastAPI микросервиса в контейнере необходимо:**

Собрать образ:

```
docker build -f Dockerfile_ml_service --tag ml_service:1 .
```

Запустить контейнер:
```
docker run --publish 8081:8081 --volume=./models:/services/models --env-file .env ml_service:1

```

Запустится контейнер с сервисом. Для тестирования работы приложения откройте новый терминал и отправьте тестовый запрос через curl:

```
curl -X POST "http://127.0.0.1:8081/predict" -H "Content-Type: application/json" -d '{
    "building_type_int": 6,
    "latitude": 55.71711349487305,
    "longitude": 37.78112030029297,
    "ceiling_height": 2.640000104904175,
    "flats_count": 84,
    "floors_total": 12,
    "has_elevator": true,
    "floor": 9,
    "kitchen_area": 9.899999618530272,
    "living_area": 19.899999618530277,
    "rooms": 1,
    "is_apartment": false,
    "total_area": 35.099998474121094,
    "build_year": 1965
}'
```

**Для запуска FastAPI микросервиса с помощью Docker compose необходимо:**

Собрать образ и запустить контейнер:

```
docker compose up --build
```

Запустится контейнер с сервисом. Для тестирования работы приложения откройте новый терминал и отправьте тестовый запрос через curl:

```
curl -X POST "http://127.0.0.1:8081/predict" -H "Content-Type: application/json" -d '{
    "building_type_int": 6,
    "latitude": 55.71711349487305,
    "longitude": 37.78112030029297,
    "ceiling_height": 2.640000104904175,
    "flats_count": 84,
    "floors_total": 12,
    "has_elevator": true,
    "floor": 9,
    "kitchen_area": 9.899999618530272,
    "living_area": 19.899999618530277,
    "rooms": 1,
    "is_apartment": false,
    "total_area": 35.099998474121094,
    "build_year": 1965
}'
```

### 3. Настройка Ptometheus и Grafana

Добавляем в docker-compose.yaml описание еще двух сервисов:

```

  prometheus:
    image: prom/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    ports:
      - "${PROMETHEUS_PORT}:${PROMETHEUS_PORT}" 
    volumes:
      - "./services//prometheus/prometheus.yml:/etc/prometheus/prometheus.yml"
    hostname: prometheus
    


  grafana:
    image: grafana/grafana
    env_file:
      - ./.env
    ports:
      - "${PORT_GRAFANA}:${PORT_GRAFANA}" 
    environment:
      - GF_SECURITY_ADMIN_USER=${GRAFANA_USER}
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    hostname: grafana

```

Также для работы prometheus напишем собственный конфиг prometheus.yml, который подключается в качестве тома в Docker:

```
global:
  scrape_interval: 15s
  scrape_timeout: 10s

scrape_configs:
  - job_name: "scrapping-main-app"
    metrics_path: /metrics
    scheme: http
    static_configs:
      - targets: 
        - ml_service:8081
```



Собрать образ и запустить контейнер:

```
docker compose up --build
```

Запустится контейнер с сервисом. Для тестирования работы приложения откройте новый терминал и отправьте тестовый запрос через curl:

```
curl -X POST "http://127.0.0.1:8081/predict" -H "Content-Type: application/json" -d '{
    "building_type_int": 6,
    "latitude": 55.71711349487305,
    "longitude": 37.78112030029297,
    "ceiling_height": 2.640000104904175,
    "flats_count": 84,
    "floors_total": 12,
    "has_elevator": true,
    "floor": 9,
    "kitchen_area": 9.899999618530272,
    "living_area": 19.899999618530277,
    "rooms": 1,
    "is_apartment": false,
    "total_area": 35.099998474121094,
    "build_year": 1965
}'
```

Для запуска веба prometheus и grafana переходим по соответствующим адресам:

```
http://localhost:9090/
http://localhost:3000/
```
