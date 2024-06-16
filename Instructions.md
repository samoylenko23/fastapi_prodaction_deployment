# Инструкции по запуску микросервиса

### 1. FastAPI микросервис в виртуальном окружение

```
python3 -m venv ./venv
source ...
uvicorn ...
```


### 2. FastAPI микросервис в Docker-контейнере

docker build -f /home/mle-user/mle-project-sprint-3-v001/services/Dockerfile_ml_service --tag ml_service:1 /home/mle-user/mle-project-sprint-3-v001/services/
