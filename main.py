""" Start this script to run alarm detection on website """
from time import sleep
from controllers import FtpUploader, WebsiteClicker

if __name__ == '__main__':
    app = WebsiteClicker()
    for i in range(10):
        print(f'Round: {i + 1}')
        app.run()
        sleep(.2)

    to_upload = [f'{filename}.json' for filename in app.reports_types]

    ftp = FtpUploader()
    ftp.run(to_upload)
