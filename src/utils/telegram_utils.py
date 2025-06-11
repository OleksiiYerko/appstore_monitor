#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import os
import base64

def get_project_root():
    """Получает путь к корневой папке проекта"""
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def load_telegram_config():
    """Загружает конфигурацию Telegram из файла или переменных окружения"""
    # Сначала проверяем переменные окружения (для GitHub Actions)
    env_token = os.environ.get('TELEGRAM_TOKEN')
    env_chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    env_topic_id = os.environ.get('TELEGRAM_TOPIC_ID')
    
    if env_token and env_chat_id:
        print("📱 Используются переменные окружения для Telegram")
        return env_token, env_chat_id, env_topic_id
    
    # Если переменных окружения нет, загружаем из файла
    config_path = os.path.join(get_project_root(), "data", "config", "telegram_config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config.get("TG_TOKEN"), config.get("TG_CHAT_ID"), config.get("TG_TOPIC_ID")
    except FileNotFoundError:
        print(f"⚠️ Файл конфигурации Telegram не найден: {config_path}")
        return "YOUR_BOT_TOKEN", "YOUR_CHAT_ID", None
    except Exception as e:
        print(f"❌ Ошибка загрузки конфигурации Telegram: {e}")
        return "YOUR_BOT_TOKEN", "YOUR_CHAT_ID", None

def load_message_ids():
    """Загружает ID сообщений из файла"""
    message_ids_path = os.path.join(get_project_root(), "data", "config", "message_ids.json")
    print(f"🔍 Загружаем message_ids из: {message_ids_path}")
    try:
        with open(message_ids_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"✅ Загружено {len(data)} message_ids: {list(data.keys())}")
            return data
    except FileNotFoundError:
        print(f"⚠️ Файл message_ids не найден, создаем пустой словарь")
        return {}
    except Exception as e:
        print(f"❌ Ошибка загрузки ID сообщений: {e}")
        return {}

def save_message_ids(message_ids):
    """Сохраняет ID сообщений в файл"""
    message_ids_path = os.path.join(get_project_root(), "data", "config", "message_ids.json")
    print(f"💾 Сохраняем {len(message_ids)} message_ids в: {message_ids_path}")
    try:
        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(message_ids_path), exist_ok=True)
        with open(message_ids_path, "w", encoding="utf-8") as f:
            json.dump(message_ids, f, ensure_ascii=False, indent=2)
        print(f"✅ Message IDs сохранены успешно")
    except Exception as e:
        print(f"❌ Ошибка сохранения ID сообщений: {e}")

def save_message_ids_to_repo(message_ids):
    """Сохраняет message_ids в репозиторий через GitHub API"""
    try:
        # Получаем токен из переменных окружения
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            print("⚠️ GITHUB_TOKEN не найден, сохраняем локально")
            return save_message_ids(message_ids)
        
        # Получаем информацию о репозитории
        repo = os.environ.get('GITHUB_REPOSITORY')
        if not repo:
            print("⚠️ GITHUB_REPOSITORY не найден, сохраняем локально")
            return save_message_ids(message_ids)
        
        # Путь к файлу в репозитории
        file_path = "data/config/message_ids.json"
        
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
        content = json.dumps(message_ids, ensure_ascii=False, indent=2)
        content_bytes = content.encode('utf-8')
        content_b64 = base64.b64encode(content_bytes).decode('utf-8')
        
        data = {
            "message": "Update message IDs for App Store monitor",
            "content": content_b64,
            "branch": "main"
        }
        
        if sha:
            data["sha"] = sha
        
        # Загружаем файл
        response = requests.put(url, headers=headers, json=data)
        
        if response.status_code in [200, 201]:
            print(f"✅ Message IDs сохранены в репозиторий: {file_path}")
            return True
        else:
            print(f"❌ Ошибка сохранения в репозиторий: {response.status_code}")
            return save_message_ids(message_ids)
            
    except Exception as e:
        print(f"❌ Ошибка сохранения в репозиторий: {e}")
        return save_message_ids(message_ids)

def load_message_ids_from_repo():
    """Загружает message_ids из репозитория через GitHub API"""
    try:
        # Получаем токен из переменных окружения
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            print("⚠️ GITHUB_TOKEN не найден, загружаем локально")
            return load_message_ids()
        
        # Получаем информацию о репозитории
        repo = os.environ.get('GITHUB_REPOSITORY')
        if not repo:
            print("⚠️ GITHUB_REPOSITORY не найден, загружаем локально")
            return load_message_ids()
        
        # Путь к файлу в репозитории
        file_path = "data/config/message_ids.json"
        
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
            print(f"✅ Message IDs загружены из репозитория: {len(data)} записей")
            return data
        else:
            print(f"⚠️ Файл не найден в репозитории, загружаем локально")
            return load_message_ids()
            
    except Exception as e:
        print(f"❌ Ошибка загрузки из репозитория: {e}")
        return load_message_ids()

def send_to_telegram(message, country=None, message_id=None):
    """Отправляет сообщение в Telegram"""
    # Загружаем конфигурацию заново
    token, chat_id, topic_id = load_telegram_config()
    
    if not token or token == "YOUR_BOT_TOKEN":
        print("⚠️ Токен Telegram не настроен")
        return None
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    if topic_id:
        data["message_thread_id"] = topic_id
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            return result["result"]["message_id"]
        else:
            print(f"❌ Ошибка Telegram API: {result}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка отправки в Telegram: {e}")
        return None

def update_message(message_id, new_text):
    """Обновляет существующее сообщение в Telegram"""
    print(f"🔄 Пытаемся обновить сообщение ID: {message_id}")
    # Загружаем конфигурацию заново
    token, chat_id, topic_id = load_telegram_config()
    
    if not token or token == "YOUR_BOT_TOKEN":
        print("⚠️ Токен Telegram не настроен")
        return False
    
    url = f"https://api.telegram.org/bot{token}/editMessageText"
    
    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": new_text,
        "parse_mode": "HTML"
    }
    
    if topic_id:
        data["message_thread_id"] = topic_id
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            print(f"✅ Сообщение {message_id} успешно обновлено")
            return True
        else:
            print(f"❌ Ошибка обновления сообщения {message_id}: {result}")
            return False
        
    except Exception as e:
        print(f"❌ Ошибка обновления сообщения в Telegram: {e}")
        return False

def format_telegram_message(country_name, table_text, update_time):
    """Форматирует сообщение для Telegram"""
    return f"""📱 <b>App Store Monitor</b>\n🌍 <b>{country_name}</b>\n⏰ <b>{update_time}</b>\n\n<pre>{table_text}</pre>\n\n#AppStore #ASO #Monitor""" 