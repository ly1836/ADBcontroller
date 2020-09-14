import inspect
import ctypes


class ThreadUtil():
    thread = None

    def __init__(self, thread):
        self.thread = thread

    def asyncRaise(self, exctype):
        tid = ctypes.c_long(self.thread.ident)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    # 停止当前初始化的线程
    def stopThread(self):
        try:
            self.asyncRaise(SystemExit)
        except Exception as ex:
            print(ex)
