from time import gmtime, strftime
import time


def c_print(msg):
    print(strftime("[%Y-%m-%d %H:%M:%S]", gmtime()), msg)


def c_delay(sec, text):
    for i in range(sec):
        print(text, sec - i, 'sec')
        time.sleep(1)
