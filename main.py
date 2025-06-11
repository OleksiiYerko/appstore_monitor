#!/usr/bin/env python3
"""
Главный скрипт для запуска различных функций мониторинга App Store
"""

import sys
import os
import argparse
import requests

# Добавляем путь к src
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
TELEGRAM_TOPIC_ID = os.environ.get('TELEGRAM_TOPIC_ID')

def send_telegram_message(message):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        if TELEGRAM_TOPIC_ID:
            data["message_thread_id"] = TELEGRAM_TOPIC_ID
        try:
            requests.post(url, data=data)
        except Exception as e:
            print(f"Ошибка отправки в Telegram: {e}")

def main():
    parser = argparse.ArgumentParser(description="App Store Monitor - Главный скрипт")
    parser.add_argument("command", choices=["search", "check", "charts", "suggestions", "test"], 
                       help="Команда для выполнения")
    parser.add_argument("--bundle-id", default=os.environ.get('BUNDLE_ID', "com.kotiuzhynskyi.CameraTranslator"),
                       help="Bundle ID приложения")
    parser.add_argument("--country", default="us", help="Код страны")
    parser.add_argument("--limit", type=int, default=250, help="Лимит результатов")
    
    args = parser.parse_args()
    
    if args.command == "search":
        from src.scrapers.search_appStore import main_loop
        import json
        
        # Загружаем ключевые слова
        project_root = os.path.dirname(__file__)
        keywords_file = os.path.join(project_root, "data", "config", "keywords.json")
        
        if not os.path.exists(keywords_file):
            print(f"❌ Файл {keywords_file} не найден!")
            return
        
        with open(keywords_file, "r", encoding="utf-8") as f:
            search_terms = json.load(f)
        
        print(f"🚀 Запуск мониторинга App Store")
        print(f"📱 Bundle ID: {args.bundle_id}")
        print(f"📄 Файл ключевых слов: {keywords_file}")
        print(f"🔍 Максимальное количество результатов: {args.limit}")
        print(f"📊 Количество ключевых слов: {len(search_terms)}")
        print("-" * 50)
        send_telegram_message(f"🚀 Запуск мониторинга App Store для {args.bundle_id} с {len(search_terms)} ключевыми словами")
        main_loop(args.bundle_id, search_terms, args.limit, keywords_file=keywords_file)
    
    elif args.command == "check":
        from src.scrapers.search_appStore import single_check
        import json
        
        # Загружаем ключевые слова
        project_root = os.path.dirname(__file__)
        keywords_file = os.path.join(project_root, "data", "config", "keywords.json")
        
        if not os.path.exists(keywords_file):
            print(f"❌ Файл {keywords_file} не найден!")
            return
        
        with open(keywords_file, "r", encoding="utf-8") as f:
            search_terms = json.load(f)
        
        print(f"🔍 Выполнение проверки App Store")
        print(f"📱 Bundle ID: {args.bundle_id}")
        print(f"📄 Файл ключевых слов: {keywords_file}")
        print(f"🔍 Максимальное количество результатов: {args.limit}")
        print(f"📊 Количество ключевых слов: {len(search_terms)}")
        print("-" * 50)
        single_check(args.bundle_id, search_terms, args.limit, keywords_file=keywords_file)
    
    elif args.command == "charts":
        from src.scrapers.charts_scraper import get_app_charts
        result = get_app_charts(args.bundle_id, args.country)
        print(f"Результат: {result}")
    
    elif args.command == "suggestions":
        from src.analyzers.get_suggestions import get_suggestions_for_app
        get_suggestions_for_app()
    
    elif args.command == "test":
        print("Запуск тестов...")
        # Можно добавить запуск тестов
        print("Тесты завершены")

if __name__ == "__main__":
    main() 