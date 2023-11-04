import logging
import time
from scripts.base_script import BaseScript


class DummyScript(BaseScript):
    def run(self):
        logging.info("Dummy script was running")
        # GameActions.direct_key_press(DIK_F7)
        time.sleep(2.5)

    def before_start(self):
        logging.info('before start')
        pass

    def after_stop(self):
        logging.info('after stop')
        pass
