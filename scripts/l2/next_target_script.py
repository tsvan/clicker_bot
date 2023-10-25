import threading
import time

from action.direct_keys import *
from action.game_actions import GameActions
from analyzers.l2.next_target import NextTargetScreenAnalyzer
from screen_maker import ScreenMaker
from scripts.base_script import BaseScript
from helpers import *

# максимальный уровень хп монстра
MAX_MOB_HP = 110
# пороговое начение хп персоонажа, при котором осуществляется лечение банкой
CHARACTER_HP_USE_HEAL = 50
CHARACTER_MAX_HP = 110

# координаты движения мышки при поиске монстра
MOB_SEARCH_FIRST_MOVE_X = 1
MOB_SEARCH_FIRST_MOVE_Y = 31
# движение мышкой по координате в поисках рамки моба
MOB_SEARCH_MOVE_TO_X = 5
MOB_SEARCH_MOVE_TO_Y = 120
# смещение для скриншота моба с рамкой
MOB_SEARCH_SCREEN_X1 = 50
MOB_SEARCH_SCREEN_X2 = 120
MOB_SEARCH_SCREEN_Y1 = 15
MOB_SEARCH_SCREEN_Y2 = 60

# максимальная попытка поиска монстра
MOB_SEARCH_MAX_COUNT = 5

# delay
DEFAULT_DELAY = 0.3

IF_MOB_NOT_FOUND_MOVE = [(670, 460), (675, 440), (630, 430)]

# координаты окна
Left_Top_X, Left_Top_Y = 1, 31
Right_Bottom_X, Right_Bottom_Y = 1279, 757
Bar_X, Bar_Y = 809, 129


class NextTargetL2Script(BaseScript):

    def __init__(self):
        self.mob_not_found_try = 0
        self.mob_max_hp_count = 0
        pass

    def before_start(self):
        c_delay(5, 'starting')
        pass

    def after_stop(self):
        pass

    def next_target_find(self):
        # F5 - next target
        GameActions.direct_key_press(DIK_F5)
        screen = ScreenMaker.get_screenshot_region(Left_Top_X, Left_Top_Y, (Bar_X - Left_Top_X),
                                              (Bar_Y - Left_Top_Y), "bar")
        mob_health = NextTargetScreenAnalyzer.get_mob_health(screen)
        if mob_health == 0:
            return False
        else:
            return True

    def find_next_mob(self, screen):
        level_text = NextTargetScreenAnalyzer.find_mob_level(screen)
        if level_text == 0:
            print('rotate')
            GameActions.rotate_camera_l2()
            # GameActions.next_target()
            time.sleep(DEFAULT_DELAY)
            return

        x, y, w, h = level_text
        if not self.move_mouse_to_find_mob(x - 10, y + MOB_SEARCH_FIRST_MOVE_Y, x + 40, y + MOB_SEARCH_MOVE_TO_Y):
            self.move_mouse_to_find_mob(x + 40, y + MOB_SEARCH_FIRST_MOVE_Y, x - 10, y + MOB_SEARCH_MOVE_TO_Y)


        screen = ScreenMaker.get_screenshot_region(Left_Top_X, Left_Top_Y, (Bar_X - Left_Top_X),
                                              (Bar_Y - Left_Top_Y), "bar")
        mob_health = NextTargetScreenAnalyzer.get_mob_health(screen)
        if mob_health == 0:
            # GameActions.direct_key_press(DIK_DOWN)
            GameActions.direct_key_press(DIK_ESCAPE)

    def move_mouse_to_find_mob(self, x1, y1, x2, y2):
        mob_screen_x1 = x1 - MOB_SEARCH_SCREEN_X1
        mob_screen_y1 = y1 - MOB_SEARCH_SCREEN_Y1
        mob_screen_x2 = x2 + MOB_SEARCH_SCREEN_X2
        mob_screen_y2 = y2 + MOB_SEARCH_SCREEN_Y2

        if not self.check_coords([x1, x2, mob_screen_x1, mob_screen_x2],
                                           [y1, y2, mob_screen_y1, mob_screen_y2]):
            print(x1, y1, x2, y2)
            return False
        GameActions.mouse_move_to(x1, y1, 0)
        t = threading.Thread(target=GameActions.mouse_move_to,
                             args=(x2, y2, 1))
        t.start()
        while t.is_alive():
            screen = ScreenMaker.get_screenshot_region(mob_screen_x1, mob_screen_y1, mob_screen_x2, mob_screen_y2, 'mob')
            targeted_bar = NextTargetScreenAnalyzer.find_mob_targeted(screen)
            if targeted_bar != 0:
                x, y = GameActions.position()
                t.join()
                GameActions.mouse_click(x, y)
                return True
        return False

    def check_coords(self, arrX, arrY):
        for x in arrX:
            if Left_Top_X > x > Right_Bottom_X:
                return False

        for y in arrY:
            if Left_Top_Y > y > Right_Bottom_Y:
                return False
        return True

    def run(self):
        screen = ScreenMaker.get_screenshot_region(Left_Top_X, Left_Top_Y, (Bar_X - Left_Top_X),
                                              (Bar_Y - Left_Top_Y), "bar")

        my_health, mob_health = NextTargetScreenAnalyzer.pixels_check(screen)

        if my_health < CHARACTER_HP_USE_HEAL:
            # use hp potion
            GameActions.direct_key_press(DIK_F8)

        if mob_health > 0:
            if self.mob_max_hp_count > 30:
                GameActions.direct_key_press(DIK_ESCAPE)
                GameActions.rotate_camera_l2()
                self.mob_max_hp_count = 0
            if mob_health > MAX_MOB_HP:
                # manor
                GameActions.direct_key_press(DIK_F6)
                # attack
                GameActions.direct_key_press(DIK_F1)
                self.mob_max_hp_count += 1
            else:
                # attack
                GameActions.direct_key_press(DIK_F1)
                self.mob_max_hp_count = 0
            self.mob_not_found_try = 0
            time.sleep(DEFAULT_DELAY)
            return

        if my_health == 0:
            print('i am dead')
            return

        # моб убит
        if mob_health == 0:
            mob_bar = NextTargetScreenAnalyzer.find_close_mob_bar_icon(screen)
            print('mob_bar', mob_bar)
            if mob_bar != 0:
                # pickUp
                GameActions.direct_key_press(DIK_F4)
                GameActions.direct_key_press(DIK_F4)
                GameActions.direct_key_press(DIK_F4)
                GameActions.direct_key_press(DIK_F4)
                GameActions.direct_key_press(DIK_F4)
                GameActions.direct_key_press(DIK_F4)
                # harvest
                GameActions.direct_key_press(DIK_F7)
                # continue
            if self.mob_not_found_try > MOB_SEARCH_MAX_COUNT:
                move_x, move_y = IF_MOB_NOT_FOUND_MOVE[random.randint(0, 2)]
                print(move_x, move_y)
                # GameActions.mouse_click(move_x, move_y)
                self.mob_not_found_try = 0
            if self.next_target_find():
                return
            # Раскоментить для запуска поиска мобов по иконке
            # screen = ScreenMaker.get_screenshot_region(Left_Top_X, Left_Top_Y, (Right_Bottom_X - Left_Top_X),
            #                                   (Right_Bottom_Y - Left_Top_Y), "next_target_main")
            #self.find_next_mob(screen)
