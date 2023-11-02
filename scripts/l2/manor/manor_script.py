from typing import Final
from action.game_actions import *
from screen.screen_service import ScreenService
from scripts.base_script import BaseScript
from screen_maker import ScreenMaker
from action.game_actions import GameActions
from helpers import *
import pytesseract
import os
import re
from itertools import cycle
from dotenv import load_dotenv

from scripts.l2.login_script import LoginScript

DEFAULT_OFFSET_X = 10
DEFAULT_DELAY: Final = 0.1

CITIES_OFFSET = {
    '0': 0,
    '1': 15,
    '2': 30,
    '3': 45,
    '4': 60,
    '5': 75,
    '6': 90,
}


class ManorL2Script(BaseScript):
    def __init__(self):
        load_dotenv()
        self.login_script = LoginScript()
        self.screen_service = ScreenService(0, 0, 1280, 800, "manor_l2")
        self.firstRun = True

        self.attempt = 0

        manor_opts = os.getenv('MANOR_OPTS')
        manor_opts = manor_opts.split(";")
        self.manor_opts_iterator = cycle(manor_opts)
        self.current_manor_opts = next(self.manor_opts_iterator)

        pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH')

        pass

    def before_start(self):
        c_delay(5, 'starting')
        pass

    def after_stop(self):
        pass

    def check_window_stage(self):
        check_button = self.screen_service.find_img_with_attempts("manor2.png", False)
        if check_button:
            check_x, check_y, w, h = check_button
            check_screen = self.screen_service.get_screenshot_region(check_x - 100, check_y - 56, 170, 56)
            config = r'--oem 3 --psm 6'
            captcha = pytesseract.image_to_string(check_screen, config=config, lang="rus+eng")
            manor_sum = self.find_check_sum(captcha)
            GameActions.type_digits(manor_sum)
            GameActions.mouse_click(check_x + DEFAULT_OFFSET_X, check_y)

    @staticmethod
    def find_check_sum(txt):
        txt = txt.split("\n")[0]
        txt = txt[0:-1]
        x, y = txt.split("+")
        return int(re.findall("\d+", x)[0]) + int(re.findall("\d+", y)[0])

    def main_window_stage(self):
        main_window = self.screen_service.find_img_with_attempts("manor1.png", True)
        if main_window:
            x, y, w, h = main_window
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y)

    def sell_window_stage(self):
        sell_window = self.screen_service.find_img_with_attempts("manor3.png", True)
        if sell_window:
            x, y, w, h = sell_window
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y + 20)
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y + 20)

    def select_city_window_stage(self):
        drop_down = self.screen_service.find_img_with_attempts("manor4.png", True)
        if drop_down:
            x, y, w, h = drop_down

            # Получаем номер города в списке и количество плодов для сдачи
            city_number, seed_count = self.current_manor_opts.split(",")

            GameActions.type_digits(seed_count)
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y)

            time.sleep(DEFAULT_DELAY)

            # select city
            city_offset = CITIES_OFFSET[city_number]
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y + 30 + city_offset)

    def accept_window_stage(self):
        accept_window = self.screen_service.find_img_with_attempts("manor_accept.png", True)
        if accept_window:
            x, y, w, h = accept_window
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y)

    def last_window_stage(self):
        last_window = self.screen_service.find_img_with_attempts("manor_sell.png", True, confidence=.9)
        if last_window:
            x, y, w, h = last_window
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y)

    def run(self):
        if self.firstRun:
            # self.login_service.start()
            self.firstRun = False
            time.sleep(1)
        try:
            self.attempt += 1
            if self.attempt > 10:
                self.attempt = 0
                print('relog')
                # self.login_service.restart()

            GameActions.direct_key_press(DIK_F2)

            self.main_window_stage()
            self.check_window_stage()
            self.sell_window_stage()
            self.select_city_window_stage()
            self.accept_window_stage()
            self.last_window_stage()

            self.attempt = 0
        except Exception as e:
            print('Exception:', str(e))
            return

        self.current_manor_opts = next(self.manor_opts_iterator)

        time.sleep(DEFAULT_DELAY)
