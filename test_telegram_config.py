#!/usr/bin/env python3
"""
Тестовый скрипт для проверки загрузки конфигурации Telegram
"""

import sys
import os

# Добавляем путь к src
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.utils.telegram_utils import load_telegram_config, send_to_telegram

print("🔧 Проверка конфигурации Telegram")
print("-" * 40)

# Загружаем конфигурацию заново
token, chat_id, topic_id = load_telegram_config()

print(f"📱 Токен: {token[:20]}..." if token and token != "YOUR_BOT_TOKEN" else "❌ Токен не настроен")
print(f"💬 Chat ID: {chat_id}")
print(f"📋 Topic ID: {topic_id}")

# Тест отправки сообщения
if token and token != "YOUR_BOT_TOKEN":
    print("\n🧪 Тестирование отправки сообщения...")
    test_message = "🧪 Тестовое сообщение от App Store Monitor\n✅ Конфигурация Telegram работает!"
    result = send_to_telegram(test_message)
    
    if result:
        print("✅ Сообщение успешно отправлено!")
    else:
        print("❌ Ошибка отправки сообщения")
else:
    print("\n❌ Токен не настроен, пропускаем тест отправки") 