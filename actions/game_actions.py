import pyautogui
from actions.direct_keys import *
import random


class GameActions:

    @staticmethod
    def mouse_click(x, y, duration=random.uniform(0.1, 0.2)):
        pyautogui.moveTo(x, y, duration)
        pyautogui.mouseDown()
        time.sleep(random.uniform(0.1, 0.2))
        pyautogui.mouseUp()

    @staticmethod
    def mouse_click_current_point(hold=random.uniform(0.1, 0.2)):
        pyautogui.mouseDown()
        time.sleep(hold)
        pyautogui.mouseUp()

    @staticmethod
    def mouse_move_to(x, y, duration=random.uniform(0.1, 0.2)):
        pyautogui.moveTo(x, y, duration)

    @staticmethod
    def key_press(key):
        pyautogui.press(key)

    # if pyautogui not working in game, can try this keyboard action
    @staticmethod
    def direct_key_press(key):
        TypeKey(key)
