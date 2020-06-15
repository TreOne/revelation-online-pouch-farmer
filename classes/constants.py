# coding=utf-8
import os
from datetime import datetime

VERSION = u"2.0"
APP_NAME = u"RevBot"
APP_NAME_ABBR = u"RB"
APP_NAME_RUS = u"RevBot"
DESCRIPTION = u"Помощник по игре Revelation"
AUTHOR = u"TreOne"
AUTHOR_EMAIL = u"tre@tre.one"
COPYRIGHT = u"Все права защищены. (c) 2018-%s %s" % (datetime.now().year, AUTHOR)

APP_NAME_WITHOUT_SPACES = APP_NAME.lower().replace(" ", "-")
CWD = os.getcwd()

PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # Каталог приложения
RESOURCES_PATH = os.path.join(PATH, "resources")

HOME_PATH = os.path.join(os.path.expanduser("~"))
USER_PATH = os.path.join(HOME_PATH, ".{}".format(APP_NAME_WITHOUT_SPACES))
IMAGES_PATH = os.path.join(USER_PATH, "images")

# Создаем пути, если они не существуют
for folder in [USER_PATH, IMAGES_PATH]:
    if not os.path.exists(folder.encode("UTF-8")):
        os.makedirs(folder)
