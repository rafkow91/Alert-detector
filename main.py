from time import sleep
from controllers import WebsiteClicker


if __name__ == '__main__':
    app = WebsiteClicker()
    for i in range(10):
        print(f'Round: {i+1}')
        app.run()
        sleep(.2)

