#!/usr/bin/env bash

# ---------------------------------------------
# Переменные, которые ДОЛЖНЫ быть заданы в env
# ---------------------------------------------

ALLURE_HOST="${ALLURE_HOST}"
SEND_PATH="${SEND_PATH}"
GENERATE_PATH="${GENERATE_PATH}"
PROJECT_ID="${PROJECT_ID}"


# (Необязательно) проверяем, что все переменные заданы.
# Если хотите, можете убрать эту проверку.
if [ -z "$ALLURE_HOST" ] || [ -z "$SEND_PATH" ] || [ -z "$GENERATE_PATH" ] || [ -z "$PROJECT_ID" ]; then
  echo "Ошибка: Не заданы необходимые переменные окружения:"
  echo "ALLURE_HOST=$ALLURE_HOST"
  echo "SEND_PATH=$SEND_PATH"
  echo "GENERATE_PATH=$GENERATE_PATH"
  echo "PROJECT_ID=$PROJECT_ID"
  exit 1
fi

SEND_URL="$ALLURE_HOST$SEND_PATH?project_id=$PROJECT_ID"
GENERATE_URL="$ALLURE_HOST$GENERATE_PATH?project_id=$PROJECT_ID"
PROJECTS_URL="$ALLURE_HOST/allure-docker-service/projects"

# Проверяем, существует ли проект
PROJECT_CHECK=$(curl -s -X GET "$PROJECTS_URL/$PROJECT_ID")

if [[ "$PROJECT_CHECK" == *"not found"* ]]; then
    echo "Проект $PROJECT_ID не найден. Создаём проект..."
    CREATE_PROJECT_RESPONSE=$(curl -s -X POST "$PROJECTS_URL" \
        -H "Content-Type: application/json" \
        -d "{\"id\": \"$PROJECT_ID\"}")

    echo "Ответ сервера при создании проекта: $CREATE_PROJECT_RESPONSE"

    if [[ "$CREATE_PROJECT_RESPONSE" == *"successfully created"* ]]; then
        echo "Проект $PROJECT_ID успешно создан."
    else
        echo "Ошибка при создании проекта $PROJECT_ID."
        echo "Ответ сервера: $CREATE_PROJECT_RESPONSE"
        # Убираем exit, чтобы продолжить выполнение в любом случае
    fi
else
    echo "Проект $PROJECT_ID уже существует."
fi

echo "Отправка результатов на: $SEND_URL"
echo "Генерация отчёта по адресу: $GENERATE_URL"

# Отправляем файлы в Allure Docker Service
for file in allure-results/*-result.json; do
  if [ -s "$file" ]; then
    FILE_NAME="$(basename "$file")"
    FILE_CONTENT="$(base64 -w 0 "$file")"

    JSON_PAYLOAD="$(jq -n --arg file_name "$FILE_NAME" --arg content_base64 "$FILE_CONTENT" \
      '{results: [{file_name: $file_name, content_base64: $content_base64}]}' )"

    curl -X POST "$SEND_URL" \
      -H "accept: application/json" \
      -H "Content-Type: application/json" \
      -d "$JSON_PAYLOAD"
  fi
done

# Генерируем отчёт автоматически
echo "Generating Allure report..."
RESPONSE="$(curl -s -X GET "$GENERATE_URL")"
REPORT_URL="$(echo "$RESPONSE" | jq -r '.data.report_url')"

if [ -n "$REPORT_URL" ] && [ "$REPORT_URL" != "null" ]; then
  echo "Отчёт сгенерирован:"
  echo "$REPORT_URL"
else
  echo "Ошибка при генерации отчета"
  echo "Ответ сервера: $RESPONSE"
fi