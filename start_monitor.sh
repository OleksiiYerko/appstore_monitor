#!/bin/bash

# Переходим в директорию проекта
cd /Users/cat/Documents/GitFolders/MyProjects/appstore_monitor

# Запускаем мониторинг
python3 main.py search >> appstore_monitor.log 2>&1 