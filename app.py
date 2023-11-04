import logging
import os
import threading
import winsound
from typing import Final
import keyboard
from bot_service import BotService

START_KEY: Final = 'S'
STOP_KEY: Final = 'Q'


class App:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt='%H:%M:%S')
        self.stop_event = threading.Event()
        self.service = BotService()
        self.stop_event.set()

    def run_script(self):
        self.service.before_start()
        logging.info(f'Script Started. To stop script press {STOP_KEY}')
        self.stop_event.clear()
        winsound.Beep(1600, 500)

    def stop(self):
        logging.warning("Script stopped")
        self.stop_event.set()
        self.service.after_stop()
        winsound.Beep(440, 500)
        os._exit(1)

    def start(self):
        logging.info(f'Press {START_KEY} to start script')
        t = threading.Thread(target=self.service.run, args=(self.stop_event,))
        t.start()
        keyboard.add_hotkey(STOP_KEY, self.stop)
        keyboard.add_hotkey(START_KEY, self.run_script)
