from typing import Final

import pyautogui

import cv2
import numpy as np

from screen_maker import ScreenMaker

MOB_HP_COLOR = (111, 23, 19)
MY_HEALTH_COLOR = (121, 28, 17)
MOB_NOT_HP_COLOR = (49, 28, 26)

# точки координат где не осуществляется поиск рамки монстра
MOB_NO_SEARCH_AREA_X1: Final = 522
MOB_NO_SEARCH_AREA_X2: Final = 774
MOB_NO_SEARCH_AREA_Y1: Final = 296
MOB_NO_SEARCH_AREA_Y2: Final = 443
# на сколько может отличаться найденая область рамки моснтра от границ
MOB_NO_SEARCH_DIFFERENCE: Final = 20

# пиксели поиска рамки монстра
MOB_SEARCH_MAX_PIXEL: Final = 255
MOB_SEARCH_MIN_PIXEL: Final = 250
MOB_SEARCH_RECT_X: Final = 20
MOB_SEARCH_RECT_Y: Final = 5


class NextTargetScreenAnalyzer:

    @staticmethod
    def find_close_mob_bar_icon(screen):
        location = pyautogui.locate(ScreenMaker.get_path_to_image('next_target_l2', "close_mob_bar.png"), screen, confidence=.9)

        if location:
            return location

        return 0

    @staticmethod
    def find_mob_attack_icon(screen):
        location = pyautogui.locate(ScreenMaker.get_path_to_image('next_target_l2', "attack_bar.png"), screen, confidence=.9)

        if location:
            return location

        return 0

    @staticmethod
    def find_mob_targeted(screen):
        location = pyautogui.locate(ScreenMaker.get_path_to_image('next_target_l2', "mob_bar_targeted.png"), screen, confidence=.6)

        if location:
            return location

        return 0

    @staticmethod
    def find_mob_level(screen):
        location = pyautogui.locate(ScreenMaker.get_path_to_image('next_target_l2', "mob_lvl.png"), screen, confidence=.7)

        if location:
            return location

        return 0

    @staticmethod
    def get_mob_health(screen):
        health = 0
        for pixel in screen.getdata():
            if pixel == MOB_HP_COLOR:
                health += 1
        return health

    @staticmethod
    def get_mob_not_health(screen):
        health = 0
        for pixel in screen.getdata():
            if pixel == MOB_NOT_HP_COLOR:
                health += 1
        return health

    @staticmethod
    def get_my_health(screen):
        health = 0
        for pixel in screen.getdata():
            if pixel == MY_HEALTH_COLOR:
                health += 1
        return health

    @staticmethod
    def pixels_check(screen):
        my_health = 0
        mob_health = 0
        for pixel in screen.getdata():
            if pixel == MY_HEALTH_COLOR:
                my_health += 1
            if pixel == MOB_HP_COLOR:
                mob_health += 1
        return my_health, mob_health

    @staticmethod
    def find_mob_name_area(screen):
        gray = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2GRAY)
        ret, threshold1 = cv2.threshold(gray, MOB_SEARCH_MIN_PIXEL, MOB_SEARCH_MAX_PIXEL, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (MOB_SEARCH_RECT_X, MOB_SEARCH_RECT_Y))
        closed = cv2.morphologyEx(threshold1, cv2.MORPH_CLOSE, kernel)
        closed = cv2.erode(closed, kernel, iterations=1)
        closed = cv2.dilate(closed, kernel, iterations=1)
        (centers, hierarchy) = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in centers:
            if cv2.contourArea(c) <= MOB_NO_SEARCH_DIFFERENCE:
                continue
            x, y, w, h = cv2.boundingRect(c)
            if (MOB_NO_SEARCH_AREA_X1 < x < MOB_NO_SEARCH_AREA_X2) \
                    and (MOB_NO_SEARCH_AREA_Y1 < y < MOB_NO_SEARCH_AREA_Y2):
                continue
            return x, y, w, h
        return 0, 0, 0, 0