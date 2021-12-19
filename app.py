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
        self.stop_event.set()

    def run_script(self):
        c_print(f'Script Started. To stop script press {STOP_KEY}')
        self.stop_event.clear()

    def stop(self):
        c_print('Script Stopped')
        self.stop_event.set()

    def start(self):
        print(f'Press {START_KEY} to start script')
        service = BotService()
        t = threading.Thread(target=service.run, args=(self.stop_event, "task"))
        t.start()
        keyboard.add_hotkey(STOP_KEY, self.stop)
        keyboard.add_hotkey(START_KEY, self.run_script)
