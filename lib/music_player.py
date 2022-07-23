class MusicPlayer:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
    
    def music_player(self, rtttl_code):
        return self._serial_wrapper.send(f"music_player {rtttl_code}")