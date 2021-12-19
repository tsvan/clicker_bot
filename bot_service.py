from scripts.test_script import *


class BotService:
    def __init__(self):
        self.script = TestScript()

    def run(self, stop_event, arg):
        while True:
            if not stop_event.is_set():
                self.script.run()
            else:
                time.sleep(1)
