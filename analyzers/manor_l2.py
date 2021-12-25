import re
import pyautogui
from screen_maker import ScreenMaker

CHECK_X = 300
CHECK_y = 361


class ManorScreenAnalyzer:
    def __init__(self):
        self.x1 = 1
        self.y1 = 31
        self.x2 = 1279
        self.y2 = 757

        self.savedPos = {
            'first': [],
            'manor_type': [],
            'select_city': [],
            'accept': [],
            'sell': [],
            'checkWindow': []

        }

    def __get_screen(self):
        return ScreenMaker.get_screenshot_region(self.x1, self.y1, self.x2, self.y2, 'manor')

    def __get_screenshot_check(self, i, pos):
        if not pos:
            return self.__get_screen()
        x, y, w, h = pos
        screen = ScreenMaker.get_screenshot_region(x + self.x1, y + self.y1, x + self.x1 + CHECK_X,
                                                   y + self.y1 + CHECK_y, 'check')
        return screen

    def find_main_window(self, count):
        if self.savedPos['first'] and count < 5:
            return self.savedPos['first']

        screen = self.__get_screen()
        location = pyautogui.locate(ScreenMaker.get_path_to_image('manor_l2', "manor1.png"), screen, confidence=.9)
        if location:
            self.savedPos['first'] = location
            return location

        return 0

    def find_check_window(self):
        if self.savedPos['checkWindow']:
            screen = self.__get_screenshot_check(1, self.savedPos['checkWindow'])

            location = pyautogui.locate(ScreenMaker.get_path_to_image('manor_l2', "manor2.png"), screen, confidence=.8)

            if location:
                x, y, w, h = location
                offset_x, offset_y, offset_w, offset_h = self.savedPos['checkWindow']
                return x + offset_x, y + offset_y, 0, 0

        screen = self.__get_screen()
        locate_check = pyautogui.locate(ScreenMaker.get_path_to_image('manor_l2', "manor_check.png"), screen,
                                        confidence=.8)
        if locate_check:
            self.savedPos['checkWindow'] = locate_check
        location = pyautogui.locate(ScreenMaker.get_path_to_image('manor_l2', "manor2.png"), screen, confidence=.8)

        if location:
            return location
        return 0

    def find_sell_window(self):
        if self.savedPos['manor_type']:
            return self.savedPos['manor_type']

        screen = self.__get_screen()
        location = pyautogui.locate(ScreenMaker.get_path_to_image('manor_l2', "manor3.png"), screen, confidence=.8)

        if location:
            self.savedPos['manor_type'] = location
            return location

        return 0

    def find_drop_down(self):
        if self.savedPos['select_city']:
            return self.savedPos['select_city']

        screen = self.__get_screen()
        location = pyautogui.locate(ScreenMaker.get_path_to_image('manor_l2', "manor4.png"), screen, confidence=.8)

        if location:
            self.savedPos['select_city'] = location
            return location

        return 0

    def find_accept_button(self):
        if self.savedPos['accept']:
            return self.savedPos['accept']

        screen = self.__get_screen()
        location = pyautogui.locate(ScreenMaker.get_path_to_image('manor_l2', "manor_accept.png"), screen,
                                    confidence=.8)

        if location:
            self.savedPos['accept'] = location
            return location

        return 0

    def find_sell_button(self):
        if self.savedPos['sell']:
            return self.savedPos['sell']

        screen = self.__get_screen()
        location = pyautogui.locate(ScreenMaker.get_path_to_image('manor_l2', "manor_sell.png"), screen, confidence=.9)

        if location:
            self.savedPos['sell'] = location
            return location

        return 0

    @staticmethod
    def find_check_sum(str):
        str = str.split("\n")[0]
        str = str[0:-1]
        x, y = str.split("+")
        return int(re.findall("\d+", x)[0]) + int(re.findall("\d+", y)[0])
