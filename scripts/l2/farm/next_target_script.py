import sys
import threading
import time

from action.direct_keys import *
from action.game_actions import GameActions
from screen_maker import ScreenMaker
from scripts.base_script import BaseScript
from helpers import *
from scripts.l2.farm.next_target_analyzer import NextTargetScreenAnalyzer
from scripts.l2.login_script import *

# максимальный уровень хп монстра
MAX_MOB_HP = 110
# пороговое начение хп персоонажа, при котором осуществляется лечение банкой
CHARACTER_HP_USE_HEAL = 50
CHARACTER_MAX_HP = 110

# максимальная попытка поиска монстра
MOB_SEARCH_MAX_COUNT = 5

# delay
DEFAULT_DELAY = 0.3

# координаты окна
Left_Top_X, Left_Top_Y = 1, 31
Bar_X, Bar_Y = 809, 129


class NextTargetL2Script(BaseScript):

    def __init__(self):
        self.login_service = LoginScript()
        # Кнопки которые использует бот
        # spoil/manor
        self.before_attack_btn = DIK_F6
        # attack
        self.attack_btn = DIK_F1
        # next_target
        self.next_target_btn = DIK_F5
        # pick up
        self.pick_up_btn = DIK_F4
        # heal potion
        self.heal_btn = DIK_F8
        # sweep/harvest
        self.after_mob_dead_btn = DIK_F7

    def before_start(self):
        c_delay(5, 'starting')
        self.login_service.move_window()
        time.sleep(2)
        pass

    def after_stop(self):
        pass

    def after_mob_dead(self):
        # pickUp
        GameActions.direct_key_press(self.pick_up_btn)
        GameActions.direct_key_press(self.pick_up_btn)
        time.sleep(DEFAULT_DELAY)
        GameActions.direct_key_press(self.pick_up_btn)
        GameActions.direct_key_press(self.pick_up_btn)
        time.sleep(DEFAULT_DELAY)
        GameActions.direct_key_press(self.pick_up_btn)
        GameActions.direct_key_press(self.pick_up_btn)
        time.sleep(DEFAULT_DELAY)
        # harvest
        GameActions.direct_key_press(self.after_mob_dead_btn)
        time.sleep(DEFAULT_DELAY)

    def run(self):
        screen = ScreenMaker.get_screenshot_region(Left_Top_X, Left_Top_Y, (Bar_X - Left_Top_X),
                                                   (Bar_Y - Left_Top_Y), "bar")

        my_health, mob_health = NextTargetScreenAnalyzer.pixels_check(screen)

        if my_health < CHARACTER_HP_USE_HEAL:
            GameActions.direct_key_press(self.heal_btn)

        if mob_health > 0:
            if mob_health > MAX_MOB_HP:
                # spoil / manor
                GameActions.direct_key_press(self.before_attack_btn)
                # attack
                GameActions.direct_key_press(self.attack_btn)
            else:
                # attack
                GameActions.direct_key_press(self.attack_btn)

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
                self.after_mob_dead()
            # next target
            GameActions.direct_key_press(self.next_target_btn)

        time.sleep(DEFAULT_DELAY)
