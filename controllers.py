""" All controllers for app Alert-detect """
from datetime import datetime
from ftplib import FTP
from json import dump, load
from os import path, remove
from time import sleep

from dotenv import dotenv_values
from pyautogui import (
    center,
    screenshot,
    locateCenterOnScreen,
    locateOnScreen,
    locateAllOnScreen,
    click,
)
import pytesseract


class WebsiteClicker():
    """
    App click on screen, read and save active reports

    Returns:
        - files (json type) for each one type of report
    """

    targets_dir = 'targets'
    check_image_path = path.join(targets_dir, 'check.png')
    close_image_path = path.join(targets_dir, 'close.png')
    exit_image_path = path.join(targets_dir, 'exit.png')
    pop_up_window_image_path = path.join(targets_dir + '/pop-up-window.png')
    screenshot_name = 'screenshot.png'
    report_screen_name = 'report.png'
    reports = []
    reports_images_path = path.join('web', 'img', 'penguins')
    reports_types = [
        'island',
        'lunch_break',
        'man_outside',
        'no_report',
        'pirates'
    ]

    def _read_screen(self):
        to_cut = (locateOnScreen(self.pop_up_window_image_path, confidence=0.5))
        screenshot(self.report_screen_name, region=to_cut)
        report_text = pytesseract.image_to_string(self.report_screen_name)
        remove(self.report_screen_name)
        return report_text

    @staticmethod
    def _save_to_json(filename: str = 'test', dict_to_save: dict = None) -> None:
        if dict_to_save is None:
            dict_to_save = {}

        context = []
        try:
            with open(f'{filename}.json', mode='r+', encoding='utf8') as input_file:
                context = load(input_file)
        except FileNotFoundError:
            pass

        context.append(dict_to_save)
        with open(f'{filename}.json', mode='w', encoding='utf8') as output_file:
            dump(context, output_file)

    def run(self) -> None:
        """
        Method to start app

        Steps:
        - take screenshot
        - check localisation button 'Sprawdź'
        - open reports, get type (from image), save details (type, reported_by, date)
            and save to json-file -> in for-loop
        """

        screenshot(self.screenshot_name)

        check_localisations = [center(box) for box in locateAllOnScreen(
            self.check_image_path, confidence=0.95)]

        remove(self.screenshot_name)
        for check_button in check_localisations:
            report = {}

            click(check_button)
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
                    report_content[report_content.index('Raportuje' or 'aportuje')
                                   + 1:report_content.index('dnia')])
                report['date'] = ' '.join(
                    report_content[report_content.index('dnia')
                                   + 2:report_content.index('dnia') + 6])
            except ValueError:
                exit_button_position = locateCenterOnScreen(self.exit_image_path, confidence=0.95)
                click(exit_button_position)
                continue

            sleep(.4)
            click(close_button_position)
            sleep(.4)

            self._save_to_json(report['type'], report)


class FtpUploader:
    """ Class to upload files on ftp-server """
    config = dotenv_values()
    dir_name = 'Alert-detect'

    def run(self, list_of_files=None):
        """
        Method to start upload

        Steps:
        - connect to FTP server (config data must be added to .env file)
        - check if folder 'Alert-detect' is existed, if not create it
        - check if folder with today's date is existed, if not create it
        - copy files from list to folder

        Keyword Arguments:
            list_of_files -- names of files to upload,
                for example ['file1.txt', 'file2.py'] (default: {[]})
        """
        if list_of_files is None:
            list_of_files = []

        today = datetime.now().strftime('%Y-%m-%d')

        with FTP(self.config['FTP_HOST'],
                 self.config['FTP_USER'],
                 self.config['FTP_PASSWORD']) as ftp:

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
