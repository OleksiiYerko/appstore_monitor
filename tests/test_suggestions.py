#!/usr/bin/env python3
"""
Тестовый скрипт для проверки поисковых подсказок
"""

import json
import sys
import os

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.scrapers.charts_scraper import get_search_suggestions, get_suggestions_for_keywords

def test_single_suggestion():
    """Тест получения подсказок для одного запроса"""
    print("🧪 Тест 1: Поиск подсказок для 'camera'")
    
    suggestions = get_search_suggestions("camera", "us")
    
    if suggestions:
        print(f"\n📋 Найдено {len(suggestions)} подсказок:")
        for i, suggestion in enumerate(suggestions[:10], 1):  # Показываем первые 10
            print(f"  {i}. {suggestion}")
        
        # Сохраняем результат
        with open("suggestions_test.json", "w", encoding="utf-8") as f:
            json.dump(suggestions, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Результат сохранен в suggestions_test.json")
    else:
        print("❌ Подсказки не найдены")

def test_multiple_keywords():
    """Тест получения подсказок для нескольких ключевых слов"""
    print("\n🧪 Тест 2: Поиск подсказок для нескольких ключевых слов")
    
    # Загружаем ключевые слова из файла
    keywords_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "config", "keywords.json")
    try:
        with open(keywords_path, "r", encoding="utf-8") as f:
            keywords_data = json.load(f)
            keywords = list(keywords_data.keys())
    except FileNotFoundError:
        print("❌ Файл keywords.json не найден")
        return
    
    # Берем первые 3 ключевых слова для теста
    test_keywords = keywords[:3]
    print(f"📝 Тестируем ключевые слова: {test_keywords}")
    
    results = get_suggestions_for_keywords(test_keywords, "us")
    
    if results:
        print(f"\n📊 Результаты:")
        for keyword, suggestions in results.items():
            print(f"\n🔍 '{keyword}': {len(suggestions)} подсказок")
            for i, suggestion in enumerate(suggestions[:5], 1):  # Показываем первые 5
                print(f"  {i}. {suggestion}")
        
        # Сохраняем результат
        with open("suggestions_multiple.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Результат сохранен в suggestions_multiple.json")
    else:
        print("❌ Подсказки не найдены")

def test_different_countries():
    """Тест подсказок в разных странах"""
    print("\n🧪 Тест 3: Сравнение подсказок в разных странах")
    
    countries = ["us", "gb", "de", "fr", "ru"]
    query = "camera"
    
    results = {}
    
    for country in countries:
        print(f"\n🌍 Проверяем страну: {country}")
        suggestions = get_search_suggestions(query, country)
        results[country] = suggestions
        
        if suggestions:
            print(f"  Найдено {len(suggestions)} подсказок")
            for i, suggestion in enumerate(suggestions[:3], 1):  # Показываем первые 3
                print(f"  {i}. {suggestion}")
        else:
            print("  Подсказки не найдены")
    
    # Сохраняем результат
    with open("suggestions_countries.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Результат сохранен в suggestions_countries.json")

if __name__ == "__main__":
    print("🚀 Запуск тестов поисковых подсказок")
    print("=" * 50)
    
    # Запускаем тесты
    test_single_suggestion()
    test_multiple_keywords()
    test_different_countries()
    
    print("\n✅ Все тесты завершены!") 