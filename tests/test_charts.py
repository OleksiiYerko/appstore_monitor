#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.scrapers.charts_scraper import get_multiple_charts, get_category_charts
from src.scrapers.charts_scraper import get_category_name

def test_charts():
    """Тестирует функционал чартов"""
    
    bundle_id = "com.kotiuzhynskyi.CameraTranslator"
    countries = ["us", "gb"]
    
    print("🎯 Тестирование функционала чартов App Store")
    print("=" * 60)
    
    for country in countries:
        print(f"\n🌍 Страна: {country.upper()}")
        print("-" * 40)
        
        # Тестируем общие чарты
        print("📊 Общие чарты:")
        charts_data = get_multiple_charts(bundle_id, country)
        
        for chart_type, data in charts_data.items():
            if data["position"]:
                print(f"  ✅ {chart_type}: #{data['position']}")
            else:
                print(f"  ❌ {chart_type}: не найдено")
        
        # Тестируем категорийные чарты
        print("\n📂 Категорийные чарты:")
        categories = [6007, 6002, 6008]  # Productivity, Utilities, Photo & Video
        
        for category_id in categories:
            category_name = get_category_name(category_id)
            result = get_category_charts(bundle_id, country, category_id)
            
            if result:
                print(f"  ✅ {category_name}: #{result['position']}")
            else:
                print(f"  ❌ {category_name}: не найдено")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    test_charts() 