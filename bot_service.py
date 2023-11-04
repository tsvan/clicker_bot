import logging
import os
from dotenv import load_dotenv
from scripts.dummy_script import *
from scripts.l2.manor.manor_script import ManorL2Script
from scripts.l2.farm.next_target_script import NextTargetL2Script

scripts = {
    "Manor": ManorL2Script,
    "NextTarget": NextTargetL2Script,
}


class BotService:
    def __init__(self):
        load_dotenv()
        self.script = scripts.get(os.getenv('SCRIPT_NAME'), DummyScript)()

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
