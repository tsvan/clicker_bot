from pathlib import Path
import pathlib
import time

import pyautogui


class ScreenService:
    def __init__(self, x, y, w, h, image_folder):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.image_folder = image_folder

        # Нужно для сохранения координат в find_img_with_attempts
        self.savedPos = {}

    def get_screenshot_window(self):
        screen = pyautogui.screenshot(region=(self.x, self.y, self.w, self.h))
        return screen

    @staticmethod
    def get_screenshot_region(x, y, w, h):
        screen = pyautogui.screenshot(region=(x, y, w, h))
        return screen

    @staticmethod
    def get_path_to_image(folder, name):
        dir_path = pathlib.Path().resolve()
        img_folder = Path(dir_path, 'images')
        path = Path(img_folder, folder, name)
        return str(path)

    @staticmethod
    def get_folder_path(folder):
        dir_path = pathlib.Path().resolve()
        path = Path(dir_path, folder)
        return str(path)

    @staticmethod
    def pixel_check(screen, checked_pixel):
        count = 0
        for pixel in screen.getdata():
            if pixel == checked_pixel:
                count += 1
        return count

    def find_img_with_attempts(self, img_name, with_save, attempts=40, timeout=0.05, confidence=.9):
        attempt = 0
        while True:
            attempt += 1
            if attempt > attempts:
                # Тут img_name как ключ в массиве сохранённых координат.
                # Если искать одинаковое изображение разными вызовами могут быть проблемы
                self.savedPos[img_name] = []
                raise TimeoutError(f"{attempt} attempts ends, img-{img_name}")

            if with_save and img_name in self.savedPos and self.savedPos[img_name]:
                x, y, w, h = self.savedPos[img_name]
                region_screen = self.get_screenshot_region(x - 10, y - 10, w + 20, h + 20)
                location = pyautogui.locate(self.get_path_to_image(self.image_folder, img_name), region_screen,
                                            confidence=confidence)
                if location:
                    return self.savedPos[img_name]

            else:
                screen = self.get_screenshot_window()
                location = pyautogui.locate(self.get_path_to_image(self.image_folder, img_name), screen,
                                            confidence=confidence)

                if location:
                    self.savedPos[img_name] = location
                    return location

            time.sleep(timeout)
