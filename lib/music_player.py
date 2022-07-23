import threading

class MusicPlayer:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
        self.thread = None
    
    def _run(self, rtttl_code):
        self._serial_wrapper.send(f"music_player {rtttl_code}")

    def play(self, rtttl_code):
        self.thread = threading.Thread(target=self._run, args=(rtttl_code,))
        self.thread.start()
    
    def stop(self):
        if self.thread.is_alive():
            self._serial_wrapper.ctrl_c()