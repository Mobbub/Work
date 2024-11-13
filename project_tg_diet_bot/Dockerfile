# Используем образ Python 3.10-slim в качестве базового
FROM python:3.10-slim

# Копирование файлов приложения
COPY project_tg_diet_bot/ /project_tg_diet_bot/
WORKDIR /project_tg_diet_bot


# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Установка зависимостей приложения
#ENV $(cat /project_tg_diet_bot/.env | xargs)
ENV BOT_TOKEN=7267663094:AAFLFlKynuoTv9X1yCydk3rXykIAIT3DJWE
ENV OPENAI_API_KEY=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
ENV DATABASE_URL=mysql+pymysql://docker:docker5WnTQeofNa1S@db/diet_bot_db


# Указываем главный скрипт для запуска
CMD ["python3", "main.py"]