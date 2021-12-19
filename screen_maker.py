import pyautogui
from pathlib import Path
import pathlib


class ScreenMaker:

    @staticmethod
    def get_folder_path(folder):
        dir_path = pathlib.Path().resolve()
        path = Path(dir_path, folder)
        return str(path)

    @staticmethod
    def get_screenshot_region(x1, y1, x2, y2, name='region'):
        screen = pyautogui.screenshot(ScreenMaker.get_folder_path('screens') + str(name) + ".png",
                                      region=(x1, y1, (x2 - x1), (y2 - y1)))
        return screen

    @staticmethod
    def get_screenshot(name='all'):
        screen = pyautogui.screenshot(ScreenMaker.get_folder_path('screens') + str(name) + ".png")
        return screen
