import time
from scripts.base_script import BaseScript


class TestScript(BaseScript):
    def run(self):
        print('run test script')
        time.sleep(1)

    def before_start(self):
        print('before start')
        pass

    def after_stop(self):
        print('after stop')
        pass

