import os
import sys

# Указываем путь к src для поиска модулей
sys.path.insert(0, os.path.abspath("../src"))

# Определяем настройки Sphinx
extensions = [
    "sphinx.ext.autodoc",  # Для автоматического извлечения документации из docstrings
    "sphinx.ext.viewcode",  # Для отображения исходного кода
]

# Исключаем тесты из сборки документации
exclude_patterns = ["tests", "static", "templates"]

# Общие настройки проекта
project = "FlasktemplateTestGitlab"  # Укажите название вашего проекта
author = "Your Name"  # Укажите автора документации
version = "0.1.0"  # Укажите версию проекта
release = "0.1.0"  # Укажите релиз проекта (может быть таким же, как версия)

# Настройка языка
language = "ru"  # Установите язык документации, если необходимо

# Настройки HTML
html_theme = "sphinx_rtd_theme"  # Вы можете изменить тему на другую, если хотите

# Настройка других опций, если требуется
htmlhelp_basename = f"{project}doc"  # Имя базы данных документации для HTMLHel
