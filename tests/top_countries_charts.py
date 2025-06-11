#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import os

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.scrapers.charts_scraper import get_app_charts
from src.utils.country_utils import get_country_name

TOP_COUNTRIES = [
    "us", "gb", "de", "fr", "it", "es", "jp", "kr", "cn", "ca",
    "au", "nl", "se", "br", "in", "mx", "tr", "ch", "pl", "sg"
]

BUNDLE_ID = "com.kotiuzhynskyi.CameraTranslator"
CHART_TYPE = "topgrossingapplications"


def main():
    print(f"\nПозиции приложения {BUNDLE_ID} в чарте {CHART_TYPE} по топ-странам:\n")
    results = []
    for country in TOP_COUNTRIES:
        country_name = get_country_name(country)
        result = get_app_charts(BUNDLE_ID, country, CHART_TYPE)
        pos = result["position"] if result and result["position"] else "-"
        results.append((country.upper(), country_name, pos))
        time.sleep(3)
    # Выводим таблицу
    print("\nРезультаты:")
    print(f"{'Страна':<8} {'Название':<25} {'Позиция':<8}")
    print("-" * 45)
    for code, name, pos in results:
        print(f"{code:<8} {name:<25} {pos:<8}")

if __name__ == "__main__":
    main() 