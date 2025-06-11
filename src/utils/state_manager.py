#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import base64
import requests
from datetime import datetime
import pytz

def get_project_root():
    """Получает путь к корневой папке проекта"""
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def load_state(filename):
    """Загружает состояние из файла"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"❌ Ошибка загрузки состояния: {e}")
    return {}

def save_state(state, filename):
    """Сохраняет состояние в файл"""
    try:
        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Ошибка сохранения состояния: {e}")

def get_now_str():
    """Возвращает текущее время в строковом формате с учетом часового пояса"""
    # Проверяем переменную окружения TZ
    timezone_str = os.environ.get('TZ', 'UTC')
    
    try:
        # Пытаемся использовать указанный часовой пояс
        tz = pytz.timezone(timezone_str)
        now = datetime.now(tz)
    except:
        # Если ошибка, используем UTC
        now = datetime.now(pytz.UTC)
    
    return now.strftime("%d %b %H:%M")

def load_table_config():
    """Загружает конфигурацию таблицы"""
    config_path = os.path.join(get_project_root(), "data", "config", "table_config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Возвращаем конфигурацию по умолчанию
        return {
            "style": "grid",
            "columns": ["KW", "Now", "UpdKW"],
            "headers": ["KW", "Now", "UpdKW"]
        }
    except Exception as e:
        print(f"❌ Ошибка загрузки конфигурации таблицы: {e}")
        return {
        "style": "grid",
            "columns": ["KW", "Now", "UpdKW"],
            "headers": ["KW", "Now", "UpdKW"]
    }

def save_table_config(config, filename="table_config.json"):
    """Сохраняет конфигурацию таблицы"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def convert_time_format(time_str):
    """Конвертирует новый формат времени в старый"""
    if not time_str or time_str == "x":
        return time_str
    
    try:
        # Пробуем распарсить новый формат "2025-06-11 01:03:22"
        new_format = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        return new_format.strftime("%d %b %H:%M")
    except:
        # Если не удалось распарсить, возвращаем как есть
        return time_str

def update_state_entry(prev_state, key, rank, timestamp):
    """Обновляет запись состояния"""
    prev_info = prev_state.get(key, {})
    
    if not isinstance(prev_info, dict):
        prev_info = {
            "initial_rank": prev_info,
            "last_rank": prev_info,
            "last_change_time": None
        }
    
    # Конвертируем новый формат времени в старый
    if prev_info.get("last_change_time"):
        prev_info["last_change_time"] = convert_time_format(prev_info["last_change_time"])
    
    # Если позиция изменилась, обновляем время последнего изменения
    if prev_info.get("last_rank") != rank:
        prev_info["last_change_time"] = timestamp
    
    # Обновляем последнюю позицию
    prev_info["last_rank"] = rank
    
    # Если это первая запись, устанавливаем начальную позицию
    if "initial_rank" not in prev_info or prev_info["initial_rank"] is None:
        prev_info["initial_rank"] = rank
    
    return prev_info 

def save_state_to_repo(state, filename="last_state.json"):
    """Сохраняет состояние в репозиторий через GitHub API"""
    try:
        # Получаем токен из переменных окружения
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            print("⚠️ GITHUB_TOKEN не найден, сохраняем локально")
            return save_state(state, filename)
        
        # Получаем информацию о репозитории
        repo = os.environ.get('GITHUB_REPOSITORY')
        if not repo:
            print("⚠️ GITHUB_REPOSITORY не найден, сохраняем локально")
            return save_state(state, filename)
        
        # Путь к файлу в репозитории
        file_path = f"data/results/{filename}"
        
        # Получаем текущий SHA файла (если существует)
        url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Проверяем, существует ли файл
        response = requests.get(url, headers=headers)
        sha = None
        if response.status_code == 200:
            sha = response.json().get("sha")
        
        # Подготавливаем данные для загрузки
        content = json.dumps(state, ensure_ascii=False, indent=2)
        content_bytes = content.encode('utf-8')
        content_b64 = base64.b64encode(content_bytes).decode('utf-8')
        
        data = {
            "message": f"Update {filename} for App Store monitor",
            "content": content_b64,
            "branch": "main"
        }
        
        if sha:
            data["sha"] = sha
        
        # Загружаем файл
        response = requests.put(url, headers=headers, json=data)
        
        if response.status_code in [200, 201]:
            print(f"✅ {filename} сохранен в репозиторий: {file_path}")
            return True
        else:
            print(f"❌ Ошибка сохранения {filename} в репозиторий: {response.status_code}")
            return save_state(state, filename)
            
    except Exception as e:
        print(f"❌ Ошибка сохранения {filename} в репозиторий: {e}")
        return save_state(state, filename)

def load_state_from_repo(filename="last_state.json"):
    """Загружает состояние из репозитория через GitHub API"""
    try:
        # Получаем токен из переменных окружения
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            print("⚠️ GITHUB_TOKEN не найден, загружаем локально")
            return load_state(filename)
        
        # Получаем информацию о репозитории
        repo = os.environ.get('GITHUB_REPOSITORY')
        if not repo:
            print("⚠️ GITHUB_REPOSITORY не найден, загружаем локально")
            return load_state(filename)
        
        # Путь к файлу в репозитории
        file_path = f"data/results/{filename}"
        
        # Получаем содержимое файла
        url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            content = response.json().get("content", "")
            content_decoded = base64.b64decode(content).decode('utf-8')
            data = json.loads(content_decoded)
            print(f"✅ {filename} загружен из репозитория: {len(data)} записей")
            return data
        else:
            print(f"⚠️ Файл {filename} не найден в репозитории, загружаем локально")
            return load_state(filename)
            
    except Exception as e:
        print(f"❌ Ошибка загрузки {filename} из репозитория: {e}")
        return load_state(filename) 