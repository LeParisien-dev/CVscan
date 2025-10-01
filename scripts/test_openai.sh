#!/usr/bin/env bash
# Simple curl test to check key (replace endpoint and model as needed)

if [ -z "$OPENAI_API_KEY" ]; then
  echo "Set OPENAI_API_KEY in your env first"
  exit 1
fi

curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"gpt-5-mini\",
    \"messages\": [{\"role\":\"user\",\"content\":\"Hello from CVScan test\"}],
    \"max_tokens\": 10
  }"
