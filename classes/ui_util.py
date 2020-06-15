# coding=utf-8
import os
from PyQt4 import uic
from classes.constants import PATH

DEFAULT_THEME_NAME = "Material"


def load_ui(window, ui_name):
    """Загружаем *.ui файл, а также XML версию файла"""
    path = os.path.join(PATH, 'resources', 'main.ui')
    # Загрузка UI из файла
    uic.loadUi(path, window)
