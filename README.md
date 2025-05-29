# 🤖 LangGraph Time Agent

Простой чат-бот с возможностью определения текущего времени.

## Запуск
```bash
# Настройка Python
git clone https://github.com/Lanutrix/LangGraph-Time-Agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Развёртывание локально Ollama
docker run -d --name ollama -p 11434:11434 -v ollama:/root/.ollama -e OLLAMA_NUM_PARALLEL=4 -e OLLAMA_MAX_LOADED_MODELS=3 --restart unless-stopped --tty ollama/ollama:latest
docker exec -it ollama ollama pull qwen2.5:7b-instruct

# Запуск проекта
langgraph dev
```


## Использование

Задайте вопрос о времени, например:
- "Который час?"
- "Какое сейчас время?"
- "What time is it?"

Бот автоматически вызовет инструмент `get_current_time` и вернет текущее UTC время.

## Требования

- Docker
- Python 3.9+

## О проекте
Это выполненное [тестовое задание](https://moonlysouls.notion.site/Python-Test-Task-1fb203040a3580c4887ce0c021b56c37)

Made by **Dmitry Odintsov**