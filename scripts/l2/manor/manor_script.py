import json
import logging
import pathlib
import sys
import time
from typing import Final
from action.game_actions import *
from screen.screen_service import ScreenService
from scripts.base_script import BaseScript
from action.game_actions import GameActions
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
        pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_PATH')

        self.login_script = LoginScript(os.getenv('GAME_PATH'), 'Asterios', 'Asterios Pride', 20, 10,
                                        GameActions.direct_key_press)

        self.screen_service = ScreenService(0, 0, 1280, 800, "manor_l2")

        self.firstRun = True
        self.attempt = 0
        self.manor_opts_iterator = {}
        self.current_manor_opts = {}
        self.seed_for_sale = {}

    def before_start(self):
        logging.info("F2 - макрос на тагрет npc. F10 - сесть/встать")
        # получаем данные куда и сколько плодов сдавать из json конфига
        self.parse_manor_opts()

        for i in range(1, 6):
            sys.stdout.write("\rStart in 5 sec. Starting %d..." % i)
            sys.stdout.flush()
            time.sleep(1)
        print('\n')

    def after_stop(self):
        pass

    def check_window_stage(self):
        # Находим окно капчи
        check_window = self.screen_service.find_img_with_attempts("manor_check.png", True)
        check_window_x, check_window_y, _, _ = check_window
        # находим кнопку капчи в окне (для быстродействия что бы не делать фул скрин)
        check_window_screen = self.screen_service.get_screenshot_region(check_window_x, check_window_y, 320, 360)
        check_button = pyautogui.locate(self.screen_service.get_path_to_image("manor_l2", "manor2.png"),
                                        check_window_screen,
                                        confidence=.9)

        if check_button:
            check_x, check_y, _, _ = check_button
            check_screen = self.screen_service.get_screenshot_region(check_x + check_window_x - 100,
                                                                     check_y + check_window_y - 56, 170, 56)
            config = r'--oem 3 --psm 6'
            captcha = pytesseract.image_to_string(check_screen, config=config, lang="rus+eng")
            manor_sum = self.find_check_sum(captcha)
            GameActions.type_digits(manor_sum)
            GameActions.mouse_click(check_x + check_window_x + DEFAULT_OFFSET_X, check_y + check_window_y)

    @staticmethod
    def find_check_sum(txt):
        txt = txt.split("\n")[0]
        txt = txt[0:-1]
        x, y = txt.split("+")
        return int(re.findall("\d+", x)[0]) + int(re.findall("\d+", y)[0])

    def parse_manor_opts(self):
        data = json.load(open(self.screen_service.get_folder_path('static') + '\\manor.json'))
        for seed in data['manor']:
            self.seed_for_sale[seed] = True
            self.manor_opts_iterator[seed] = cycle(data['manor'][seed])
            self.current_manor_opts[seed] = next(self.manor_opts_iterator[seed])
            logging.info(f'ПЛОД: {seed}:')
            for city_opt in data['manor'][seed]:
                logging.info(f"номер города:{city_opt['city_number']} количество семян:{city_opt['seed_count']}")

    def select_city_window_stage(self, seed):
        drop_down = self.screen_service.find_img_with_attempts("manor4.png", True)
        if drop_down:
            x, y, w, h = drop_down

            # Получаем номер города в списке и количество плодов для сдачи
            self.current_manor_opts[seed] = next(self.manor_opts_iterator[seed])

            GameActions.type_digits(self.current_manor_opts[seed]['seed_count'])
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y)

            time.sleep(DEFAULT_DELAY)

            # select city
            city_offset = CITIES_OFFSET[self.current_manor_opts[seed]['city_number']]
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y + 30 + city_offset)

    def select_seeds(self):
        sell_window = self.screen_service.find_img_with_attempts("manor3.png", True)
        x, y, w, h = sell_window
        i = 1
        for seed in self.seed_for_sale:
            seed_x = x + DEFAULT_OFFSET_X
            seed_y = y + 20 * i

            # Проверка не закончились ли плоды (по белому пикселю в названии плода)
            check_seed_screen = self.screen_service.get_screenshot_region(seed_x - 5, seed_y - 2, seed_x + 50,
                                                                          seed_y + 2)
            seed_exist = self.screen_service.pixel_check(check_seed_screen, (215, 215, 215))
            if seed_exist > 0:
                GameActions.mouse_click(seed_x, seed_y)
                GameActions.mouse_click(seed_x, seed_y)
            else:
                return

            self.select_city_window_stage(seed)
            accept_window = self.screen_service.find_img_with_attempts("manor_accept.png", True)
            x2, y2, _, _ = accept_window
            GameActions.mouse_click(x2 + DEFAULT_OFFSET_X, y2)
            i += 1
            time.sleep(DEFAULT_DELAY)

    def check_unexpected_window(self):
        window = self.screen_service.get_screenshot_window()
        location = pyautogui.locate(self.screen_service.get_path_to_image("manor_l2", "manor_cancel.png"), window,
                                    confidence=0.9)
        if location:
            logging.warning('Find unexpected window')
            x, y, _, _ = location
            GameActions.mouse_click(x + DEFAULT_OFFSET_X, y + 5)

    def run(self):
        if self.firstRun:
            self.login_script.start()
            self.firstRun = False
            time.sleep(1)
        try:
            self.attempt += 1
            if self.attempt > 10:
                self.attempt = 0
                logging.info('relog')
                self.login_script.restart()

            # Жмём макрос на таргет npc менеджера
            GameActions.direct_key_press(DIK_F2)
            # Кликаем на кнопку сдачи манора
            main_window_x, main_window_y, _, _ = self.screen_service.find_img_with_attempts("manor1.png", True)
            GameActions.mouse_click(main_window_x + DEFAULT_OFFSET_X, main_window_y)
            # Проверка капчи
            self.check_window_stage()
            # Вводим количество плод для каждого плода
            self.select_seeds()
            # Нажимаем продать плоды
            last_window_x, last_window_y, _, _ = self.screen_service.find_img_with_attempts("manor_sell.png", True)
            GameActions.mouse_click(last_window_x + DEFAULT_OFFSET_X, last_window_y)

            self.attempt = 0
        except Exception as e:
            logging.error(f"ManorException {str(e)}")
            # Проверка если что то багнуло и окно от преидущей сдачи не закрылось
            self.check_unexpected_window()
            return
