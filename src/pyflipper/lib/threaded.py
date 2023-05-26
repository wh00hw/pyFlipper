from threading import Thread
import time


class Threaded:
    def __init__(self) -> None:
        self.thread = None

    def exec(self, func, timeout: int):
        assert bool(func) or bool(timeout), "func or timeout required"
        def _timer():
            time.sleep(timeout)
            self.stop()
        if func:
            #function thread execution
            self.thread = Thread(target=func)
            self.thread.start()
        if timeout:
            #force ctr-c when expires
            timer = Thread(target=_timer)
            timer.start()
            if not func:
                self.thread = timer

    def stop(self) -> None:
        if self.thread.is_alive():
            self._serial_wrapper.ctrl_c()
            self.thread = None
