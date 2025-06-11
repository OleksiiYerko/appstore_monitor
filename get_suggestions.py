#!/usr/bin/env python3
"""
Скрипт для получения поисковых подсказок по ключевым словам приложения
"""

import json
import time
from datetime import datetime
from charts_scraper import get_suggestions_for_keywords

def load_keywords_and_countries():
    """Загружает ключевые слова и список стран из файла"""
    try:
        with open("keywords.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            keywords = list(data.keys())
            # Собираем уникальные страны из значений
            countries = set()
            for v in data.values():
                countries.update(v)
            # Удаляем 'ru' если вдруг есть
            countries.discard('ru')
            return keywords, sorted(countries)
    except FileNotFoundError:
        print("❌ Файл keywords.json не найден")
        return [], []

def get_suggestions_for_app():
    """Получает подсказки для ключевых слов приложения"""
    
    # Загружаем ключевые слова и страны
    keywords, countries = load_keywords_and_countries()
    if not keywords:
        print("❌ Ключевые слова не найдены")
        return
    if not countries:
        print("❌ Страны не найдены в keywords.json")
        return
    
    print(f"📝 Найдено {len(keywords)} ключевых слов: {keywords}")
    print(f"🌍 Будут использоваться только страны из keywords.json: {countries}")
    
    all_results = {}
    
    for country in countries:
        print(f"\n🌍 Анализ страны: {country}")
        print("=" * 40)
        
        country_results = get_suggestions_for_keywords(keywords, country)
        all_results[country] = country_results
        
        # Показываем краткую сводку
        total_suggestions = sum(len(suggestions) for suggestions in country_results.values())
        print(f"📊 Всего подсказок для страны {country}: {total_suggestions}")
        
        # Пауза между странами
        time.sleep(5)
    
    # Сохраняем результаты
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"suggestions_app_{timestamp}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Результаты сохранены в {filename}")
    
    # Анализируем результаты
    analyze_suggestions(all_results, keywords)

def analyze_suggestions(results, keywords):
    """Анализирует полученные подсказки"""
    print(f"\n📊 АНАЛИЗ РЕЗУЛЬТАТОВ")
    print("=" * 50)
    
    # Ищем упоминания "translator" или "translation"
    translator_mentions = {}
    
    for country, country_results in results.items():
        translator_mentions[country] = []
        
        for keyword, suggestions in country_results.items():
            for suggestion in suggestions:
                term = suggestion.get("term", "").lower()
                if "translator" in term or "translation" in term:
                    translator_mentions[country].append({
                        "keyword": keyword,
                        "suggestion": suggestion["term"]
                    })
    
    # Показываем результаты
    print("🎯 Найдены подсказки с упоминанием 'translator' или 'translation':")
    
    for country, mentions in translator_mentions.items():
        if mentions:
            print(f"\n🌍 {country}:")
            for mention in mentions:
                print(f"  • '{mention['keyword']}' → '{mention['suggestion']}'")
        else:
            print(f"\n🌍 {country}: Нет упоминаний")
    
    # Создаем сводный отчет
    summary = {
        "total_countries": len(results),
        "total_keywords": len(keywords),
        "translator_mentions": translator_mentions,
        "timestamp": datetime.now().isoformat()
    }
    
    summary_filename = f"suggestions_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_filename, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Сводный отчет сохранен в {summary_filename}")

if __name__ == "__main__":
    print("🚀 Запуск анализа поисковых подсказок для приложения")
    print("=" * 60)
    
    get_suggestions_for_app()
    
    print("\n✅ Анализ завершен!") 