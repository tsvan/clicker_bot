import pyautogui
import win32api
import win32con

from actions.direct_keys import *
import random


class GameActions:

    @staticmethod
    def mouse_click(x, y,  duration=random.uniform(0.05, 0.1)):
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()
        time.sleep(duration)
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

    @staticmethod
    def type_digits(number):
        arr = map(int, str(number))
        dictionary = {
            0: DIK_0,
            1: DIK_1,
            2: DIK_2,
            3: DIK_3,
            4: DIK_4,
            5: DIK_5,
            6: DIK_6,
            7: DIK_7,
            8: DIK_8,
            9: DIK_9,
        }
        for digit in arr:
            TypeKey(dictionary[digit])

    @staticmethod
    def rotate_camera_l2():
        pyautogui.mouseDown(button='right')
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 100, 0, 0, 0)
        pyautogui.mouseUp(button='right')

    @staticmethod
    def position():
        return pyautogui.position()
