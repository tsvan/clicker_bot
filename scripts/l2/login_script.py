import ctypes
import logging
import os
import time

import pyautogui
import win32con
import win32gui
from dotenv import load_dotenv

from action.direct_keys import DIK_ENTER, DIK_F10
from action.game_actions import GameActions
from screen.screen_service import ScreenService

user32 = ctypes.windll.user32

DEFAULT_OFFSET_X = 10
DEFAULT_OFFSET_Y = 10


class LoginScript:
    def __init__(self, game_path, l2_server, l2_server_name, game_start_delay, after_login_delay, after_login_action):
        self.path = game_path
        self.l2_server = l2_server
        self.l2_server_name = l2_server_name
        self.screen_service = ScreenService(0, 0, 1280, 900, "l2_login")

        self.game_start_delay = game_start_delay
        self.after_login_delay = after_login_delay
        self.after_login_action = after_login_action

    def _login_actions(self):
        login1_x, login1_y, _, _ = self.screen_service.find_img_with_attempts("login1.png", False, 20, 1, confidence=.8)
        time.sleep(1)
        GameActions.mouse_click(login1_x + DEFAULT_OFFSET_X, login1_y + DEFAULT_OFFSET_Y, 0.3)
        GameActions.mouse_click(login1_x + DEFAULT_OFFSET_X, login1_y + DEFAULT_OFFSET_Y, 0.3)

        #Проверка если зависает при входе, закрываем окно.
        time.sleep(5)
        screen = self.screen_service.get_screenshot_window()
        cancel_screen = pyautogui.locate(self.screen_service.get_path_to_image("l2_login", "login_cancel.png"), screen,confidence=0.8)
        if cancel_screen:
            cancel_x, cancel_y,_,_ = cancel_screen
            # кликаем отмену и потом релог на шаг 1
            GameActions.mouse_click(cancel_x + DEFAULT_OFFSET_X, cancel_y + DEFAULT_OFFSET_Y, 0.3)
            time.sleep(2)
            login1_x, login1_y, _, _ = self.screen_service.find_img_with_attempts("login1.png", False, 20, 1,confidence=.8)
            time.sleep(1)
            GameActions.mouse_click(login1_x + DEFAULT_OFFSET_X, login1_y + DEFAULT_OFFSET_Y, 0.3)
            GameActions.mouse_click(login1_x + DEFAULT_OFFSET_X, login1_y + DEFAULT_OFFSET_Y, 0.3)

        login2_x, login2_y, _, _ = self.screen_service.find_img_with_attempts("login2.png", False, 20, 1, confidence=.8)
        time.sleep(1)
        GameActions.mouse_click(login2_x + DEFAULT_OFFSET_X, login2_y + DEFAULT_OFFSET_Y, 0.3)

        login3_x, login3_y, _, _ = self.screen_service.find_img_with_attempts("login3.png", False, 20, 1, confidence=.8)
        time.sleep(1)
        GameActions.mouse_click(login3_x + DEFAULT_OFFSET_X, login3_y + DEFAULT_OFFSET_Y, 0.3)

        login4_x, login4_y, _, _ = self.screen_service.find_img_with_attempts("login4.png", False, 20, 1, confidence=.8)
        time.sleep(1)
        GameActions.mouse_click(login4_x + DEFAULT_OFFSET_X, login4_y + DEFAULT_OFFSET_Y, 0.3)

        time.sleep(self.after_login_delay)
        self.after_login_action(DIK_F10)
        time.sleep(1)

    def start(self):
        os.startfile(self.path)
        time.sleep(self.game_start_delay)
        login_hwnd = win32gui.FindWindow(None, self.l2_server)
        if not login_hwnd:
            logging.exception("can't start game")
            return

        user32.MoveWindow(login_hwnd, 0, 0, 1296, 839, False)
        time.sleep(2)

        try:
            self._login_actions()
        except Exception as e:
            logging.exception('Login Exc:', str(e))
            return

    def restart(self):
        crash_hwnd = win32gui.FindWindow(None, 'LineageII Crash Report')
        if crash_hwnd:
            win32gui.PostMessage(crash_hwnd, win32con.WM_CLOSE, 0, 0)
        time.sleep(1)
        login_hwnd = win32gui.FindWindow(None, self.l2_server)
        if login_hwnd:
            win32gui.PostMessage(login_hwnd, win32con.WM_CLOSE, 0, 0)
        time.sleep(1)
        main_hwnd = win32gui.FindWindow(None, self.l2_server_name)
        if main_hwnd:
            win32gui.PostMessage(main_hwnd, win32con.WM_CLOSE, 0, 0)

        time.sleep(1)

        self.start()

    def move_window(self):
        login_hwnd = win32gui.FindWindow(None, self.l2_server)
        if login_hwnd:
            user32.MoveWindow(login_hwnd, 0, 0, 1296, 839, False)
            time.sleep(3)
