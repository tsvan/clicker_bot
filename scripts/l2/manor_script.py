from typing import Final
from analyzers.l2.manor import ManorScreenAnalyzer
from action.game_actions import *
from scripts.base_script import BaseScript
from screen_maker import ScreenMaker
from action.game_actions import GameActions
from helpers import *
import pytesseract
import os
from dotenv import load_dotenv

from scripts.l2.login_service import LoginService

DEFAULT_OFFSET_X = 10
DEFAULT_OFFSET_Y = 35

# delay
DEFAULT_DELAY: Final = 0.3
DEFAULT_MIN_DELAY: Final = 0.1

CITIES = {
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
        self.analyzer = ManorScreenAnalyzer()
        self.login_service = LoginService()
        self.firstRun = True
        self.main_delay = 1
        self.min_delay = 0.5
        self.check_button_appear = 0

        pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH')

        pass

    def before_start(self):
        c_delay(5, 'starting')
        pass

    def after_stop(self):
        pass

    def check_window_stage(self, ):
        check_button = self.analyzer.find_check_window()
        if check_button:
            self.check_button_appear = 0
            check_x, check_y, w, h = check_button
            check_screen = ScreenMaker.get_screenshot_region(check_x - 100, check_y - 25, check_x + 100,
                                                             check_y + 31, 'check_manor')
            config = r'--oem 3 --psm 6'
            str = pytesseract.image_to_string(check_screen, config=config, lang="rus+eng")
            try:
                manor_sum = self.analyzer.find_check_sum(str)
                print(manor_sum)
            except Exception as e:
                print('count sum exc')
                return False
            GameActions.mouse_click(check_x - 15, check_y + DEFAULT_OFFSET_Y)
            GameActions.type_digits(manor_sum)
            GameActions.mouse_click(check_x + DEFAULT_OFFSET_X, check_y + DEFAULT_OFFSET_Y)
            return True
        return False

    def main_window_stage(self):
        main_window = self.analyzer.find_main_window(self.check_button_appear)
        if main_window:
            x, y, w, h = main_window
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y + DEFAULT_OFFSET_Y)
            return True
        return False

    def sell_window_stage(self):
        sell_window = self.analyzer.find_sell_window()
        if sell_window:
            x, y, w, h = sell_window
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y + DEFAULT_OFFSET_Y + 15)
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y + DEFAULT_OFFSET_Y + 15)

    def last_window_stage(self):
        drop_down = self.analyzer.find_drop_down()
        if drop_down:
            x, y, w, h = drop_down
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y + DEFAULT_OFFSET_Y)
            time.sleep(self.min_delay)
            # select city
            number = CITIES[os.getenv('CITY_NUMBER')]
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y + 65 + number)
            # select count
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y + 60)
            GameActions.type_digits(os.getenv('SEED_COUNT'))
            # press accept
            accept_button = self.analyzer.find_accept_button()
            x, y, w, h = accept_button
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y + 45)
            time.sleep(self.min_delay)
            # press sell
            sell_button = self.analyzer.find_sell_button()
            if sell_button:
                x, y, w, h = sell_button
                GameActions.mouse_click(x + DEFAULT_OFFSET_X, y + DEFAULT_OFFSET_Y)

    def run(self):
        # get_cursor_position()
        # check_button = self.analyzer.find_check_window()
        # time.sleep(1)
        # return
        if self.firstRun:
            # self.login_service.start()
            self.main_delay = 1
            self.min_delay = 0.5
            self.firstRun = False
        else:
            self.main_delay = 0.2
            self.min_delay = 0.1
        try:
            if self.check_button_appear < 100:
                self.check_button_appear += 1
            self.main_window_stage()
            time.sleep(self.main_delay)
            self.check_window_stage()
            time.sleep(self.main_delay)
            self.sell_window_stage()
            time.sleep(self.main_delay)
            self.last_window_stage()
            time.sleep(self.main_delay)
            GameActions.direct_key_press(DIK_F2)
            if self.check_button_appear > 15:
                # self.login_service.restart()
                self.check_button_appear = 0
        except Exception as e:
            print('some exc', e.with_traceback())
            return
        time.sleep(self.main_delay)
