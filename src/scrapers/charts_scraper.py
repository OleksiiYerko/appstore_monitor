#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import sys
import os
import time

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.utils.country_utils import get_country_name

def get_app_charts(bundle_id: str, country: str = "us", chart_type: str = "topfreeapplications"):
    """
    Получает информацию о позиции приложения в чартах App Store
    
    Args:
        bundle_id: ID приложения
        country: Код страны (us, gb, etc.)
        chart_type: Тип чарта (topfreeapplications, toppaidapplications, newapplications, etc.)
    
    Returns:
        dict: Информация о позиции в чарте
    """
    try:
        country_name = get_country_name(country)
        print(f"📊 Проверка чарта {chart_type} | Страна: {country_name}...")

        node_code = f"""
        import store from 'app-store-scraper';
        
        store.list({{
            country: "{country}",
            category: 0,  // Все категории
            collection: "{chart_type}",
            num: 200
        }}).then(results => {{
            console.log(JSON.stringify(results));
        }}).catch(err => {{
            console.error("ERR", err.message);
            process.exit(1);
        }});
        """

        result = subprocess.run(
            ["node", "--input-type=module", "-e", node_code],
            check=True,
            capture_output=True,
            text=True
        )

        apps = json.loads(result.stdout)

        for idx, app in enumerate(apps):
            if app.get("appId") == bundle_id:
                print(f"✅ Найдено в чарте {chart_type}! Позиция: #{idx + 1}")
                return {
                    "position": idx + 1,
                    "chart_type": chart_type,
                    "country": country,
                    "total_apps": len(apps),
                    "app_info": {
                        "name": app.get("title", ""),
                        "rating": app.get("score", 0),
                        "reviews": app.get("reviews", 0),
                        "price": app.get("price", "Free")
                    }
                }

        print(f"❌ Не найдено в чарте {chart_type}")
        return None

    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка Node.js при получении чарта {chart_type}:", e.stderr)
        return None
    except Exception as e:
        print(f"❌ Ошибка Python при получении чарта {chart_type}:", str(e))
        return None

def get_multiple_charts(bundle_id: str, country: str = "us"):
    """
    Получает информацию по нескольким чартам для одной страны
    
    Returns:
        dict: Результаты по всем чартам
    """
    charts = {
        "topfreeapplications": "Топ бесплатных",
        "toppaidapplications": "Топ платных",
        "newapplications": "Новые приложения",
        "topgrossingapplications": "Топ по доходам"
    }
    
    results = {}
    
    for chart_type, chart_name in charts.items():
        result = get_app_charts(bundle_id, country, chart_type)
        if result:
            results[chart_type] = result
        else:
            results[chart_type] = {
                "position": None,
                "chart_type": chart_type,
                "country": country,
                "total_apps": 0,
                "app_info": {}
            }
    
    return results

def get_category_charts(bundle_id: str, country: str = "us", category_id: int = 6007):
    """
    Получает информацию о позиции в категорийном чарте
    
    Args:
        bundle_id: ID приложения
        country: Код страны
        category_id: ID категории (6007 = Productivity, 6002 = Utilities, etc.)
    
    Returns:
        dict: Информация о позиции в категории
    """
    try:
        country_name = get_country_name(country)
        print(f"📊 Проверка категории {category_id} | Страна: {country_name}...")

        node_code = f"""
        import store from 'app-store-scraper';
        
        store.list({{
            country: "{country}",
            category: {category_id},
            collection: "topfreeapplications",
            num: 200
        }}).then(results => {{
            console.log(JSON.stringify(results));
        }}).catch(err => {{
            console.error("ERR", err.message);
            process.exit(1);
        }});
        """

        result = subprocess.run(
            ["node", "--input-type=module", "-e", node_code],
            check=True,
            capture_output=True,
            text=True
        )

        apps = json.loads(result.stdout)

        for idx, app in enumerate(apps):
            if app.get("appId") == bundle_id:
                print(f"✅ Найдено в категории! Позиция: #{idx + 1}")
                return {
                    "position": idx + 1,
                    "category_id": category_id,
                    "country": country,
                    "total_apps": len(apps),
                    "app_info": {
                        "name": app.get("title", ""),
                        "rating": app.get("score", 0),
                        "reviews": app.get("reviews", 0)
                    }
                }

        print(f"❌ Не найдено в категории {category_id}")
        return None

    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка Node.js при получении категории {category_id}:", e.stderr)
        return None
    except Exception as e:
        print(f"❌ Ошибка Python при получении категории {category_id}:", str(e))
        return None

# Словарь категорий App Store
CATEGORIES = {
    6000: "Business",
    6001: "Weather",
    6002: "Utilities",
    6003: "Travel",
    6004: "Sports",
    6005: "Social Networking",
    6006: "Reference",
    6007: "Productivity",
    6008: "Photo & Video",
    6009: "News",
    6010: "Navigation",
    6011: "Music",
    6012: "Lifestyle",
    6013: "Health & Fitness",
    6014: "Games",
    6015: "Finance",
    6016: "Entertainment",
    6017: "Education",
    6018: "Books",
    6019: "Medical",
    6020: "Newsstand",
    6021: "Catalogs",
    6022: "Food & Drink",
    6023: "Shopping",
    6024: "Stickers",
    6025: "Developer Tools",
    6026: "Graphics & Design",
    6027: "Video Players & Editors",
    6028: "Magazines & Newspapers",
    6029: "Entertainment",
    6030: "Developer Tools",
    6031: "Graphics & Design",
    6032: "Video Players & Editors",
    6033: "Magazines & Newspapers",
    6034: "Entertainment",
    6035: "Developer Tools",
    6036: "Graphics & Design",
    6037: "Video Players & Editors",
    6038: "Magazines & Newspapers",
    6039: "Entertainment",
    6040: "Developer Tools",
    6041: "Graphics & Design",
    6042: "Video Players & Editors",
    6043: "Magazines & Newspapers",
    6044: "Entertainment",
    6045: "Developer Tools",
    6046: "Graphics & Design",
    6047: "Video Players & Editors",
    6048: "Magazines & Newspapers",
    6049: "Entertainment",
    6050: "Developer Tools"
}

def get_category_name(category_id: int):
    """Получает название категории по ID"""
    return CATEGORIES.get(category_id, f"Category {category_id}")

def get_app_info(bundle_id: str, country: str = "us"):
    """
    Получает детальную информацию о приложении
    
    Args:
        bundle_id: ID приложения
        country: Код страны
    
    Returns:
        dict: Детальная информация о приложении
    """
    try:
        country_name = get_country_name(country)
        print(f"📱 Получение информации о приложении | Страна: {country_name}...")

        node_code = f"""
        import store from 'app-store-scraper';
        
        store.app({{
            id: "{bundle_id}",
            country: "{country}"
        }}).then(result => {{
            console.log(JSON.stringify(result));
        }}).catch(err => {{
            console.error("ERR", err.message);
            process.exit(1);
        }});
        """

        result = subprocess.run(
            ["node", "--input-type=module", "-e", node_code],
            check=True,
            capture_output=True,
            text=True
        )

        app_data = json.loads(result.stdout)
        
        if app_data:
            print(f"✅ Информация получена: {app_data.get('title', 'Unknown')}")
            return {
                "title": app_data.get("title", ""),
                "developer": app_data.get("developer", ""),
                "category": app_data.get("category", ""),
                "rating": app_data.get("score", 0),
                "reviews": app_data.get("reviews", 0),
                "price": app_data.get("price", "Free"),
                "version": app_data.get("version", ""),
                "size": app_data.get("size", ""),
                "updated": app_data.get("updated", ""),
                "description": app_data.get("description", "")[:200] + "..." if len(app_data.get("description", "")) > 200 else app_data.get("description", "")
            }
        else:
            print("❌ Информация о приложении не найдена")
            return None

    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка Node.js при получении информации о приложении:", e.stderr)
        return None
    except Exception as e:
        print(f"❌ Ошибка Python при получении информации о приложении:", str(e))
        return None 

def get_search_suggestions(query: str, country: str = "us"):
    """
    Получает поисковые подсказки для запроса
    
    Args:
        query: Поисковый запрос
        country: Код страны
    
    Returns:
        list: Список подсказок
    """
    try:
        country_name = get_country_name(country)
        print(f"🔍 Поиск подсказок для '{query}' | Страна: {country_name}...")

        node_code = f"""
        import store from 'app-store-scraper';
        
        store.suggest({{
            term: "{query}",
            country: "{country}"
        }}).then(results => {{
            console.log(JSON.stringify(results));
        }}).catch(err => {{
            console.error("ERR", err.message);
            process.exit(1);
        }});
        """

        result = subprocess.run(
            ["node", "--input-type=module", "-e", node_code],
            check=True,
            capture_output=True,
            text=True
        )

        suggestions = json.loads(result.stdout)
        
        if suggestions:
            print(f"✅ Найдено {len(suggestions)} подсказок")
            return suggestions
        else:
            print("❌ Подсказки не найдены")
            return []

    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка Node.js при получении подсказок:", e.stderr)
        return []
    except Exception as e:
        print(f"❌ Ошибка Python при получении подсказок:", str(e))
        return []

def get_suggestions_for_keywords(keywords: list, country: str = "us"):
    """
    Получает подсказки для списка ключевых слов
    
    Args:
        keywords: Список ключевых слов
        country: Код страны
    
    Returns:
        dict: Словарь с подсказками для каждого ключевого слова
    """
    results = {}
    
    for keyword in keywords:
        print(f"\n📝 Обработка ключевого слова: '{keyword}'")
        suggestions = get_search_suggestions(keyword, country)
        results[keyword] = suggestions
        
        # Пауза между запросами
        time.sleep(3)
    
    return results 