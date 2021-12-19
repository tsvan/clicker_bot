import time
from scripts.base_script import BaseScript
from screen_maker import ScreenMaker

class TestScript(BaseScript):
    def run(self):
        path = ScreenMaker.get_folder_path('screens')
        print(path)
        time.sleep(1)

    def before_start(self):
        print('before start')
        pass

    def after_stop(self):
        print('after stop')
        pass

