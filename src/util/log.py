DEBUG = True

def debug(msg, *args, **kwargs):
    if DEBUG:
        print(msg, *args, **kwargs)