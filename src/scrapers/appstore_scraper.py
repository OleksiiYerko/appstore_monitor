#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import sys
import os

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.utils.country_utils import get_country_name

def get_rank(search_term: str, target_bundle_id: str, country: str = "us", max_results: int = 250):
    """Получает позицию приложения в App Store по ключевому слову"""
    try:
        country_name = get_country_name(country)
        print(f"🔍 Проверка: '{search_term}' | Страна: {country_name}...")

        node_code = f"""
        import store from 'app-store-scraper';
        store.search({{
            term: {json.dumps(search_term)},
            country: "{country}",
            num: {max_results}
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
            if app.get("appId") == target_bundle_id:
                print(f"✅ Найдено! Позиция: #{idx + 1}")
                return idx + 1

        print("❌ Не найдено в результатах")
        return None

    except subprocess.CalledProcessError as e:
        print("❌ Ошибка Node.js:", e.stderr)
        return None
    except Exception as e:
        print("❌ Ошибка Python:", str(e))
        return None

def search_app_in_store(search_term: str, bundle_id: str, country: str = "us", max_results: int = 250):
    """Алиас для get_rank для обратной совместимости"""
    return get_rank(search_term, bundle_id, country, max_results) 