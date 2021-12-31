import time

from actions.game_actions import GameActions
from actions.direct_keys import *
from scripts.base_script import BaseScript
from screen_maker import ScreenMaker

class TestScript(BaseScript):
    def run(self):
        GameActions.direct_key_press(DIK_F7)
        #print(path)
        time.sleep(2)

    def before_start(self):
        print('before start')
        pass

    def after_stop(self):
        print('after stop')
        pass

