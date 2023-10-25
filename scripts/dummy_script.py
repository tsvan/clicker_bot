import time
from scripts.base_script import BaseScript
from helpers import *


class DummyScript(BaseScript):
    def run(self):
        print("Dummy script was running")
        # GameActions.direct_key_press(DIK_F7)
        time.sleep(2.5)

    def before_start(self):
        print('before start')
        pass

    def after_stop(self):
        print('after stop')
        pass
