from .threaded import Threaded

class MusicPlayer(Threaded):
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
        super().__init__()

    def play(self, rtttl_code: str, duration: int = 10):
        def _run():
            self._serial_wrapper.send(f"music_player {rtttl_code}")
        self.exec(func=_run, timeout=duration)
    
    def beep(self, duration: float = 0.2):
        self.play("Beep:d=8,o=5,b=80:2b5", duration=duration)
