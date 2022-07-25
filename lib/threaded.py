from threading import Thread
import time


class Threaded:
    def __init__(self) -> None:
        self.thread = None

    def exec(self, func, callback, timeout: int):
        def _run():
            data = func()
            if data and callback:
                callback(data)
        def _timer():
            time.sleep(timeout)
            self.stop()
        if not self.thread:
            self.thread = Thread(target=_run)
            self.thread.start()
            if timeout:
                Thread(target=_timer).start()

    def stop(self):
        if self.thread.is_alive():
            self._serial_wrapper.ctrl_c()
            self.thread = None
