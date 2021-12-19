from time import gmtime, strftime


def c_print(msg):
    print(strftime("[%Y-%m-%d %H:%M:%S]", gmtime()), msg)
