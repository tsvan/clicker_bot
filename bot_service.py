from scripts.test_script import *
from scripts.manor_l2_script import ManorL2Script


class BotService:
    def __init__(self):
        self.script = TestScript()

    def before_start(self):
        self.script.before_start()

    def after_stop(self):
        self.script.after_stop()

    def run(self, stop_event):
        while True:
            if not stop_event.is_set():
                self.script.run()
            else:
                time.sleep(1)
