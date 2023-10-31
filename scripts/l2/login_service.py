import ctypes
import os
import time

import win32con
import win32gui
from dotenv import load_dotenv

from action.direct_keys import DIK_ENTER, DIK_F10
from action.game_actions import GameActions

user32 = ctypes.windll.user32

LOGIN_BUTTONS_X = 583
LOGIN_BUTTON_POS = 543
AGREE_LOGIN_BUTTON_POS = 613
ACCEPT_LOGIN_BUTTON_POS = 616

LOGIN_DELAY = 10
GAME_START_DELAY = 30
L2_SERVER = 'Asterios'
L2_SERVER_NAME = 'Asterios Pride'


class LoginService:
    def __init__(self):
        load_dotenv()
        self.path = os.getenv('GAME_PATH')
        self.l2_server = L2_SERVER
        self.l2_server_name = L2_SERVER_NAME

    def start(self):
        os.startfile(self.path)
        time.sleep(GAME_START_DELAY)

        login_hwnd = win32gui.FindWindow(None, self.l2_server)
        if login_hwnd:
            user32.MoveWindow(login_hwnd, 0, 0, 1296, 839, False)
            time.sleep(LOGIN_DELAY)
            GameActions.mouse_click(LOGIN_BUTTONS_X, LOGIN_BUTTON_POS, 0.3)
            GameActions.mouse_click(LOGIN_BUTTONS_X, LOGIN_BUTTON_POS, 0.3)
            time.sleep(LOGIN_DELAY)
            GameActions.mouse_click(LOGIN_BUTTONS_X, AGREE_LOGIN_BUTTON_POS, 0.3)
            time.sleep(LOGIN_DELAY)
            GameActions.mouse_click(LOGIN_BUTTONS_X, ACCEPT_LOGIN_BUTTON_POS, 0.3)
            time.sleep(LOGIN_DELAY)
            GameActions.direct_key_press(DIK_ENTER)
            time.sleep(LOGIN_DELAY)
            time.sleep(LOGIN_DELAY)
            GameActions.direct_key_press(DIK_F10)
            time.sleep(LOGIN_DELAY)

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
