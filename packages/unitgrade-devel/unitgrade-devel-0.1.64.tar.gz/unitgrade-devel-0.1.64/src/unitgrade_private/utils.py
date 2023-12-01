"""
Tue: This may become part of unitgrade proper at some point. It will allow automatic timeout of tests, but right now it is used
to timeout hidden tests which ends up in an infinite loop.

"""
import sys
import threading
from time import sleep
# try:
#     import thread
# except ImportError:
import _thread as thread

def quit_function(fn_name):
    # print to stderr, unbuffered in Python 2.
    # print('{0} took too long'.format(fn_name), file=sys.stderr)
    # sys.stderr.flush() # Python 3 stderr is likely buffered.
    thread.interrupt_main() # raises KeyboardInterrupt

def exit_after(s):
    '''
    use as decorator to exit process if
    function takes longer than s seconds
    '''
    def outer(fn):
        def inner(*args, **kwargs):
            result = 0
            try:
                timer = threading.Timer(s, quit_function, args=[fn.__name__])
                timer.start()
                try:
                    result = fn(*args, **kwargs)
                finally:
                    timer.cancel()
            except KeyboardInterrupt as e:
                print("The function took to long and is being killed.")
                args[0].assertEqual(1,2, msg="Function took to long so I am killing it.")
            return result
        return inner
    return outer
