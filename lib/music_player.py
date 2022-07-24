from threading import Thread
import time

class MusicPlayer:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
        self.thread = None

    def play(self, rtttl_code, timeout=10):
        def _run():
            self._serial_wrapper.send(f"music_player {rtttl_code}")
        def _timer(timeout):
            if self.thread.is_alive():
                time.sleep(timeout)
                self.stop()
        self.thread = Thread(target=_run)
        self.thread.start()
        if timeout:
            Thread(target=_timer, args=(timeout,)).start()

    def stop(self):
        if self.thread.is_alive():
            self._serial_wrapper.ctrl_c()
