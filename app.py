import threading
from typing import Final
import keyboard
from bot_service import BotService
from helpers import *

START_KEY: Final = 'S'
STOP_KEY: Final = 'Q'


class App:
    def __init__(self):
        self.stop_event = threading.Event()
        self.service = BotService()
        if not self.service.run_on_start:
            self.stop_event.set()
        else:
            self.service.before_start()

    def run_script(self):
        self.service.before_start()
        c_print(f'Script Started. To stop script press {STOP_KEY}')
        self.stop_event.clear()

    def stop(self):
        c_print('Script Stopped')
        self.stop_event.set()
        self.service.after_stop()

    def start(self):
        print(f'Press {START_KEY} to start script')
        t = threading.Thread(target=self.service.run, args=(self.stop_event,))
        t.start()
        keyboard.add_hotkey(STOP_KEY, self.stop)
        keyboard.add_hotkey(START_KEY, self.run_script)
