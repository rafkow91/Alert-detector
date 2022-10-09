from time import sleep
from pynput.mouse import Controller, Button
from pyautogui import center, screenshot, locateCenterOnScreen, locateOnScreen, locateAllOnScreen
from os import path, remove
import pytesseract
from json import dump, load

from ftplib import FTP
from dotenv import dotenv_values
from datetime import datetime


class WebsiteClicker():
    def __init__(self) -> None:
        self.targets_dir = 'targets'
        self.check_image_path = path.join(self.targets_dir, 'check.png')
        self.close_image_path = path.join(self.targets_dir, 'close.png')
        self.exit_image_path = path.join(self.targets_dir, 'exit.png')
        self.pop_up_window_image_path = path.join(self.targets_dir + '/pop-up-window.png')
        self.screenshot_name = 'screenshot.png'
        self.report_screen_name = 'report.png'
        self.mouse = Controller()
        self.reports = []
        self.reports_images_path = path.join('web', 'img', 'penguins')
        self.reports_types = [
            'island',
            'lunch_break',
            'man_outside',
            'no_report',
            'pirates'
        ]

    def _click_button(self, position) -> None:
        try:
            self.mouse.position = position
            self.mouse.click(Button.left, 1)
        except TypeError:
            pass

    def _read_screen(self) -> dict:
        to_cut = (locateOnScreen(self.pop_up_window_image_path, confidence=0.5))
        screenshot(self.report_screen_name, region=to_cut)
        report_text = pytesseract.image_to_string(self.report_screen_name)
        remove(self.report_screen_name)
        return report_text

    def _save_to_JSON(self, filename: str = 'test', dict_to_save: dict = {}) -> None:
        context = []
        try:
            with open(f'{filename}.json', mode='r+') as input_file:
                context = load(input_file)
        except FileNotFoundError:
            pass
        context.append(dict_to_save)
        with open(f'{filename}.json', mode='w') as output_file:
            dump(context, output_file)

    def run(self) -> None:
        screenshot(self.screenshot_name)

        check_localisations = [center(box) for box in locateAllOnScreen(
            self.check_image_path, confidence=0.95)]

        remove(self.screenshot_name)
        for check_button in check_localisations:
            report = {}
            self._click_button(check_button)
            sleep(.4)
            try:
                close_button_position = locateCenterOnScreen(self.close_image_path, confidence=0.95)
            except TypeError:
                remove(self.screenshot_name)
                screenshot(self.screenshot_name)
                check_localisations = locateAllOnScreen(self.check_image_path, confidence=0.95)
                continue

            for image in self.reports_types:
                if locateOnScreen(path.join(self.reports_images_path, f'{image}.png')) is not None:
                    report['type'] = image

            try:
                report['type']
            except KeyError:
                continue

            sleep(.4)
            report_content = self._read_screen().split()

            try:
                report['reports'] = ' '.join(
                    report_content[report_content.index('Raportuje' or 'aportuje')+1:report_content.index('dnia')])
                report['date'] = ' '.join(
                    report_content[report_content.index('dnia')+2:report_content.index('dnia')+6])
            except ValueError:
                exit_button_position = locateCenterOnScreen(self.exit_image_path, confidence=0.95)
                self._click_button(exit_button_position)
                continue

            sleep(.4)
            self._click_button(close_button_position)
            sleep(.4)

            self._save_to_JSON(report['type'], report)


class FtpUploader:
    config = dotenv_values()
    dir_name = 'Alert-detect'

    def run(self, list_of_files: list = []):
        today = datetime.now().strftime('%Y-%m-%d')

        with FTP(self.config['FTP_HOST'], self.config['FTP_USER'], self.config['FTP_PASSWORD']) as ftp:

            if self.dir_name not in ftp.nlst():
                ftp.mkd(self.dir_name)
            ftp.cwd(self.dir_name)

            if today not in ftp.nlst():
                ftp.mkd(today)
            ftp.cwd(today)

            for filename in list_of_files:
                try:
                    with open(filename, mode='rb') as to_upload:
                        ftp.storbinary(f'STOR {filename}', to_upload)
                except FileNotFoundError:
                    continue
