#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import logging
from datetime import datetime
from collections import defaultdict
from tabulate import tabulate
import sys
import os

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.scrapers.appstore_scraper import get_rank
from src.utils.country_utils import get_country_name
from src.utils.telegram_utils import load_message_ids, save_message_ids, send_to_telegram, format_telegram_message, load_telegram_config, update_message, load_message_ids_from_repo, save_message_ids_to_repo
from src.utils.state_manager import load_state, save_state, get_now_str, load_table_config, update_state_entry, load_state_from_repo, save_state_to_repo

def countdown(seconds, message="Ожидание"):
    """Обратный отсчет с сообщением"""
    for remaining in range(seconds, 0, -1):
        h, m, s = remaining // 3600, (remaining % 3600) // 60, remaining % 60
        sys.stdout.write(f"\r{message}: {h:02}:{m:02}:{s:02} ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 40 + "\r")  # очистка строки

def format_rank_display(prev_rank, rank):
    """Форматирует отображение позиции"""
    if prev_rank != rank and prev_rank is not None:
        return f"#{prev_rank} → #{rank}" if rank else f"#{prev_rank} → x"
    elif prev_rank is None and rank is not None:
        return f"x → #{rank}"
    else:
        return f"#{rank}" if rank else "x"

def main_loop(bundle_id, search_terms, limit, keywords_file=None):
    """Основной цикл мониторинга"""
    # Загружаем конфигурацию Telegram
    token, chat_id = load_telegram_config()
    print(f"📱 Telegram конфигурация загружена: токен {'настроен' if token and token != 'YOUR_BOT_TOKEN' else 'не настроен'}")
    
    # Обновляем пути к файлам
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    state_file = os.path.join(project_root, "data", "results", "last_state.json")
    
    # Проверяем, есть ли GITHUB_TOKEN для использования репозитория
    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        # Загружаем состояние из репозитория (для GitHub Actions)
        prev_state = load_state_from_repo()
        # Загружаем message_ids из репозитория (для GitHub Actions)
        message_ids = load_message_ids_from_repo()
    else:
        # Локальное использование
        prev_state = load_state(state_file)
        message_ids = load_message_ids()
    
    # Перечитываем keywords_file, если он задан
    if keywords_file:
        with open(keywords_file, "r", encoding="utf-8") as f:
            search_terms = json.load(f)
    
    # Читаем конфиг таблицы
    table_config = load_table_config()
    style = table_config["style"]
    columns = table_config["columns"]
    headers = table_config["headers"]
    
    print(f"🚀 Запуск мониторинга... (таблица: {style}, колонки: {columns})")
    print("⏰ Интервал проверки: 10 минут")
    print("🔄 Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    iteration = 0
    while True:
        iteration += 1
        print(f"\n🔄 Итерация #{iteration} - {get_now_str()}")
        
        grouped_results = defaultdict(list)
        current_state = {}
        now_str = get_now_str()

        for term, countries in search_terms.items():
            for country in countries:
                key = f"{country.lower()}|{term}"
                prev_info = prev_state.get(key, {})
                
                if not isinstance(prev_info, dict):
                    prev_info = {
                        "initial_rank": prev_info,
                        "last_rank": prev_info,
                        "last_change_time": None
                    }
                
                prev_rank = prev_info.get("last_rank")
                rank = get_rank(term, bundle_id, country, limit)
                
                # Обновляем состояние
                current_state[key] = update_state_entry(prev_state, key, rank, now_str)
                
                # Формируем данные для таблицы
                state_info = current_state[key]
                initial_rank = state_info["initial_rank"]
                last_change_time = state_info.get("last_change_time", "x")
                
                grouped_results[country.upper()].append({
                    "#": None,  # будет добавлен позже
                    "KW": term,
                    "Init": f"#{initial_rank}" if initial_rank else "x",
                    "Now": format_rank_display(prev_rank, rank),
                    "UpdKW": last_change_time if last_change_time else "x"
                })
                
                # Короткая пауза между запросами
                time.sleep(2)

        # Отправляем результаты в Telegram
        for country in sorted(grouped_results.keys()):
            country_items = grouped_results[country]
            
            # Добавляем номер, если есть колонка '#'
            if "#" in columns:
                for idx, item in enumerate(country_items):
                    item["#"] = idx + 1
            
            # Формируем строки таблицы по выбранным колонкам
            table = [
                [item[col] for col in columns]
                for item in sorted(country_items, key=lambda x: int(x["Now"].split("#")[-1].split()[0]) if "#" in x["Now"] else float("inf"))
            ]
            
            text_table = tabulate(table, headers=headers, tablefmt=style)
            country_key = country.upper()
            country_name = get_country_name(country)
            country_update_time = get_now_str()
            
            message_text = format_telegram_message(country_name, text_table, country_update_time)
            
            # Всегда отправляем новое сообщение
            new_msg_id = send_to_telegram(message_text, country=country_key)
            if new_msg_id:
                message_ids[country_key] = new_msg_id
                print(f"✅ Новое сообщение для {country_name} отправлено")
            else:
                print(f"❌ Ошибка отправки сообщения для {country_name}")
        
        # Сохраняем состояние
        if github_token:
            # Сохраняем в репозиторий (для GitHub Actions)
            save_message_ids_to_repo(message_ids)
            save_state_to_repo(current_state)
        else:
            # Локальное сохранение
            save_message_ids(message_ids)
            save_state(current_state, state_file)
        
        # Обновляем prev_state для следующей итерации
        prev_state = current_state
        
        print(f"✅ Итерация #{iteration} завершена")
        print("⏰ Ожидание 1 час до следующей проверки...")
        countdown(3600, "Ожидание")

def single_check(bundle_id, search_terms, limit, keywords_file=None):
    """Однократная проверка мониторинга (для GitHub Actions)"""
    # Загружаем конфигурацию Telegram
    token, chat_id = load_telegram_config()
    print(f"📱 Telegram конфигурация загружена: токен {'настроен' if token and token != 'YOUR_BOT_TOKEN' else 'не настроен'}")
    
    # Обновляем пути к файлам
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    state_file = os.path.join(project_root, "data", "results", "last_state.json")
    
    # Загружаем состояние из репозитория (для GitHub Actions)
    prev_state = load_state_from_repo()
    
    # Загружаем message_ids из репозитория (для GitHub Actions)
    message_ids = load_message_ids_from_repo()
    
    # Перечитываем keywords_file, если он задан
    if keywords_file:
        with open(keywords_file, "r", encoding="utf-8") as f:
            search_terms = json.load(f)
    
    # Читаем конфиг таблицы
    table_config = load_table_config()
    style = table_config["style"]
    columns = table_config["columns"]
    headers = table_config["headers"]
    
    print(f"🔍 Выполнение проверки... (таблица: {style}, колонки: {columns})")
    grouped_results = defaultdict(list)
    current_state = {}
    now_str = get_now_str()

    for term, countries in search_terms.items():
        for country in countries:
            key = f"{country.lower()}|{term}"
            prev_info = prev_state.get(key, {})
            
            if not isinstance(prev_info, dict):
                prev_info = {
                    "initial_rank": prev_info,
                    "last_rank": prev_info,
                    "last_change_time": None
                }
            
            prev_rank = prev_info.get("last_rank")
            rank = get_rank(term, bundle_id, country, limit)
            
            # Обновляем состояние
            current_state[key] = update_state_entry(prev_state, key, rank, now_str)
            
            # Формируем данные для таблицы
            state_info = current_state[key]
            initial_rank = state_info["initial_rank"]
            last_change_time = state_info.get("last_change_time", "x")
            
            grouped_results[country.upper()].append({
                "#": None,  # будет добавлен позже
                "KW": term,
                "Init": f"#{initial_rank}" if initial_rank else "x",
                "Now": format_rank_display(prev_rank, rank),
                "UpdKW": last_change_time if last_change_time else "x"
            })
            
            # Короткая пауза между запросами
            time.sleep(2)

    # Отправляем результаты в Telegram
    for country in sorted(grouped_results.keys()):
        country_items = grouped_results[country]
        
        # Добавляем номер, если есть колонка '#'
        if "#" in columns:
            for idx, item in enumerate(country_items):
                item["#"] = idx + 1
        
        # Формируем строки таблицы по выбранным колонкам
        table = [
            [item[col] for col in columns]
            for item in sorted(country_items, key=lambda x: int(x["Now"].split("#")[-1].split()[0]) if "#" in x["Now"] else float("inf"))
        ]
        
        text_table = tabulate(table, headers=headers, tablefmt=style)
        country_key = country.upper()
        country_name = get_country_name(country)
        country_update_time = get_now_str()
        
        message_text = format_telegram_message(country_name, text_table, country_update_time)
        
        # Всегда отправляем новое сообщение
        new_msg_id = send_to_telegram(message_text, country=country_key)
        if new_msg_id:
            message_ids[country_key] = new_msg_id
            print(f"✅ Новое сообщение для {country_name} отправлено")
        else:
            print(f"❌ Ошибка отправки сообщения для {country_name}")
    
    # Сохраняем состояние в репозиторий (для GitHub Actions)
    save_message_ids_to_repo(message_ids)
    save_state_to_repo(current_state)
    
    print("✅ Проверка завершена")

if __name__ == "__main__":
    # Фиксированные параметры
    bundle_id = "my.app.video.translator"
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    keywords_file = os.path.join(project_root, "data", "config", "keywords.json")
    limit = 250

    # Проверяем существование файла с ключевыми словами
    if not os.path.exists(keywords_file):
        print(f"❌ Файл {keywords_file} не найден!")
        sys.exit(1)

    with open(keywords_file, "r", encoding="utf-8") as f:
        search_terms = json.load(f)

    print(f"🚀 Запуск мониторинга App Store")
    print(f"📱 Bundle ID: {bundle_id}")
    print(f"📄 Файл ключевых слов: {keywords_file}")
    print(f"🔍 Максимальное количество результатов: {limit}")
    print(f"📊 Количество ключевых слов: {len(search_terms)}")
    print("-" * 50)

    main_loop(bundle_id, search_terms, limit, keywords_file=keywords_file)
