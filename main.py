# -*- coding: utf-8 -*-
import json
import sys
import urllib
from time import sleep

import cv2
import pyautogui
import pytesseract as pytesseract
from PyQt4 import QtGui
import os
from PyQt4 import uic
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QPixmap, QIcon, QApplication

from classes.constants import RESOURCES_PATH

pyautogui.FAILSAFE = True

question_image_path = os.path.join(RESOURCES_PATH, 'images', 'q.png')
open_profile_img_path = os.path.join(RESOURCES_PATH, 'images', 'open_profile.png')
profile_close_img_path = os.path.join(RESOURCES_PATH, 'images', 'profile_close.png')
no_bag_img_path = os.path.join(RESOURCES_PATH, 'images', 'no_bag.png')
like_btn_img_path = os.path.join(RESOURCES_PATH, 'images', 'like.png')
start_pos = {}

POS_RADIO_1 = (355, 162)
POS_RADIO_2 = (445, 162)
POS_RADIO_3 = (532, 162)

POS_FIRST_ITEM = (220, 235)


def main():
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    app.main_window = window
    ui_path = os.path.join(RESOURCES_PATH, 'main.ui')
    uic.loadUi(ui_path, window)

    # Устанавливаем иконку окна приложения
    app_icon_path = os.path.join(RESOURCES_PATH, 'images', 'university.ico')
    window.setWindowIcon(QIcon(app_icon_path))

    # Устанавливаем картинку по умолчанию для окна просмотра
    rev_logo_path = os.path.join(RESOURCES_PATH, 'images', 'rev-logo.png')
    window.preview.setPixmap(QPixmap(rev_logo_path))

    # Подключаем кнопки
    window.find_start_pos_btn.clicked.connect(on_find_start_pos_btn_clicked)
    window.start_stop_btn.clicked.connect(on_start_stop_btn_clicked)

    # Запускаем отображение относительных координат мышки
    app.main_window.pos_finder_thread = RelativePosFinder()
    app.main_window.pos_finder_thread.start()

    window.show()

    #DEBUG
    window.move(2000, 200)
    on_find_start_pos_btn_clicked()

    sys.exit(app.exec_())


def on_find_start_pos_btn_clicked():
    main_window = QApplication.instance().main_window
    header_img_path = os.path.join(RESOURCES_PATH, 'images', 'rate_list.png')

    header_pos = pyautogui.locateCenterOnScreen(header_img_path, grayscale=True, confidence=0.9)
    if header_pos:
        start_pos['x'] = header_pos.x-365
        start_pos['y'] = header_pos.y-32
        main_window.message.setText(u'Окно "Рейтинг игроков": {}х{}'.format(header_pos.x, header_pos.y))
    else:
        main_window.message.setText(u'Окно "Рейтинг игроков" НЕ ОБНАРУЖЕНО!')


def on_start_stop_btn_clicked():
    # Активируем окно игры
    relative_click((0, 0), fast=True)
    sleep(1)

    for position in range(10, 200, 10):
        scroll_list(distance=14, direction='down')  # Быстро прокручиваем список
        correct_position(position)  # Подгоняем список так, чтобы нужная позиция оказалась вверху

        first_item_pos = find_position(position)
        offset = 37
        for i in range(9):
            pyautogui.moveTo(first_item_pos.x, first_item_pos.y + offset * i)
            click('right')

            open_profile_pos = None
            while not open_profile_pos:
                open_profile_pos = pyautogui.locateCenterOnScreen(open_profile_img_path, grayscale=True, confidence=0.9)

            pyautogui.moveTo(open_profile_pos.x, open_profile_pos.y)
            click()
            while not is_profile_open():
                sleep(0.1)
            # Забираем мешочек
            if is_there_a_pouch():
                take_pouch()
            close_profile()



    # scroll_list(distance=16, direction='down')
    # sleep(2)
    # scroll_list(distance=19, direction='down')
    # sleep(2)
    # scroll_list(distance=19, direction='down')




    # # Активируем окно игры
    # relative_click((0, 0), fast=True)
    # sleep(3)
    #
    # # Забираем мешочек
    # if is_profile_open():
    #     if is_there_a_pouch():
    #         take_pouch()
    #     close_profile()


    # open_profile_btn_img_path = os.path.join(RESOURCES_PATH, 'images', 'open_profile.png')
    # like_btn_img_path = os.path.join(RESOURCES_PATH, 'images', 'like.png')
    # profile_close_img_path = os.path.join(RESOURCES_PATH, 'images', 'profile_close.png')
    #
    # relative_click((0, 0))
    #
    # offset = 17
    # for i in range(19):
    #     x, y = POS_FIRST_ITEM
    #     item_offset = 37
    #     for j in range(9):
    #         sleep(0.5)
    #         relative_move((x, y + item_offset * j), fast=True)
    #
    #         click('right')
    #
    #         open_profile_btn_pos = pyautogui.locateCenterOnScreen(open_profile_btn_img_path, grayscale=True, confidence=0.9)
    #         if open_profile_btn_pos:
    #             pyautogui.moveTo(open_profile_btn_pos.x, open_profile_btn_pos.y)
    #             click()
    #             sleep(0.5)
    #
    #         like_btn_pos = pyautogui.locateCenterOnScreen(like_btn_img_path, grayscale=True, confidence=0.9)
    #         if like_btn_pos:
    #             pyautogui.moveTo(like_btn_pos.x, like_btn_pos.y)
    #             click()
    #
    #         profile_close_btn_pos = pyautogui.locateCenterOnScreen(profile_close_img_path, grayscale=True, confidence=0.9)
    #         if profile_close_btn_pos:
    #             pyautogui.moveTo(profile_close_btn_pos.x, profile_close_btn_pos.y)
    #             click()
    #
    #     if i == 0:
    #         relative_move((650, 225), fast=True)
    #         sleep(2)
    #     else:
    #         relative_move((650, 240+offset*(i-1)), fast=True)
    #         sleep(2)
    #     relative_drag_to((650, 240+offset*i))


def find_position(digit):
    u"""Находит координаты игрока под номером оканчивающимся на заданную цифру"""
    img_name = '{:03}.png'.format(digit)
    imp_path = os.path.join(RESOURCES_PATH, 'images', 'nums', img_name)
    if os.path.exists(imp_path):
        position_pos = pyautogui.locateCenterOnScreen(imp_path, grayscale=True, confidence=0.9)
        if position_pos:
            return position_pos
    return None


def take_pouch():
    u"""Забрать мешочек если есть"""
    if is_there_a_pouch():
        like_btn_pos = pyautogui.locateCenterOnScreen(like_btn_img_path, grayscale=True, confidence=0.9)
        if like_btn_pos:
            pyautogui.moveTo(like_btn_pos.x, like_btn_pos.y)
            click()


def is_there_a_pouch():
    u"""Проверяет есть ли мешочек с наградой за лайки в профиле."""
    if not is_profile_open():
        return False
    no_bag_img_pos = pyautogui.locateCenterOnScreen(no_bag_img_path, grayscale=True, confidence=0.9)
    return False if no_bag_img_pos else True


def is_profile_open():
    u"""Проверяет открыт ли профиль."""
    profile_close_btn_pos = pyautogui.locateCenterOnScreen(profile_close_img_path, grayscale=True, confidence=0.9)
    return True if profile_close_btn_pos else False


def close_profile():
    u"""Закрыть профиль"""
    profile_close_btn_pos = pyautogui.locateCenterOnScreen(profile_close_img_path, grayscale=True, confidence=0.9)
    if profile_close_btn_pos:
        pyautogui.moveTo(profile_close_btn_pos.x, profile_close_btn_pos.y)
        click()


def relative_click(new_pos, fast=False, button='left'):
    u"""Кликает мышкой в координатах относительно окна 'Рейтинга игроков'"""
    relative_move(new_pos, fast)
    click(button)


def relative_move(new_pos, fast=False):
    u"""Перемещает мышку в координатах относительно окна 'Рейтинга игроков'"""
    x, y = new_pos
    if start_pos:
        if fast:
            pyautogui.moveTo(start_pos['x']+x, start_pos['y']+y)
        else:
            pyautogui.moveTo(start_pos['x']+x, start_pos['y']+y, 0.5, pyautogui.easeOutQuad)


def click(button='left'):
    u"""Кликает мышкой с задержкой, чтобы игра успела обработать клик"""
    pyautogui.mouseDown(button=button)
    sleep(0.2)
    pyautogui.mouseUp(button=button)


def scroll_list(distance=1, direction='down'):
    u"""Прокручивает список на заданное расстояние."""
    if direction == 'down':
        relative_move((650, 563), fast=True)
    else:
        relative_move((650, 215), fast=True)
    for i in range(distance):
        click()


def need_to_scroll_down(digit):
    u"""Нужно ли корректировать позицию списка игроков"""
    position = find_position(digit)
    if position:
        _, y = convert_to_relative(position)
        return y > 250
    else:
        return False


def convert_to_relative(position):
    u"""Возаращает координаты относительно окна 'Рейтинг игроков'."""
    return position.x-start_pos['x'], position.y-start_pos['y']


def correct_position(position):
    u"""Корректирует позицию в списке, прокручивая его вниз, пока нужная позиция не будет в верху списка."""
    while True:
        if need_to_scroll_down(position):
            scroll_list()
        else:
            break


def relative_drag_to(new_pos):
    x, y = new_pos
    sleep(0.5)
    if start_pos:
        pyautogui.dragTo(start_pos['x']+x, start_pos['y']+y, 3)


# def on_find_start_pos_btn_clicked():
#     main_window = QApplication.instance().main_window
#     question = unicode(main_window.question.toPlainText())
#     if question:
#         main_window.preview.setPixmap(QPixmap(question_image_path))
#         main_window.question.setText(question)
#         answer = get_answer(question)
#         main_window.answer.setText(answer if answer else u'Ответ не найден')


# def on_start_stop_btn_clicked():
#     main_window = QApplication.instance().main_window
#     question = get_question()
#     if question:
#         main_window.preview.setPixmap(QPixmap(question_image_path))
#         main_window.question.setText(question)
#         answer = get_answer(question)
#         main_window.answer.setText(answer if answer else u'Ответ не найден')


def get_question():
    close_btn_img_path = os.path.join(RESOURCES_PATH, 'images', 'close_btn.png')

    close_btn_pos = pyautogui.locateCenterOnScreen(close_btn_img_path, grayscale=True, confidence=0.9)
    if close_btn_pos:
        question_color_image = pyautogui.screenshot(region=(close_btn_pos.x - 390, close_btn_pos.y + 45, 390, 150))
        question_color_image.save(question_image_path)
        question_image = cv2.imread(question_image_path)
        question_image = cv2.cvtColor(question_image, cv2.COLOR_RGB2GRAY)
        _, question_image = cv2.threshold(question_image, 100, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        cv2.imwrite(question_image_path, question_image)
        question = pytesseract.image_to_string(question_image, lang='rus').replace('\n', ' ')
        return question
    else:
        return None


def get_answer(question):
    request = urllib.quote(question.encode('utf8'), safe='')
    response = urllib.urlopen("https://revclub.ru/index.php?term={}".format(request))
    data = json.load(response)

    if data:
        answers = []
        for item in data:
            answers.append(item[u'answer'])
        return u'\n'.join(answers)
    else:
        return None


class RelativePosFinder(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        main_window = QApplication.instance().main_window
        while True:
            if start_pos:
                x = pyautogui.position().x - start_pos['x']
                y = pyautogui.position().y - start_pos['y']
                main_window.statusbar.showMessage(u'{},{}'.format(x, y))
                sleep(0.2)


if __name__ == '__main__':
    main()
