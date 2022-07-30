class Update:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
    
    def install(self, fuf_file: str) -> str:
        assert fuf_file.endswith('.fuf')
        return self._serial_wrapper.send(f"update install {fuf_file}")
    
    def backup(self, destination_tar_file: str) -> str:
        assert destination_tar_file.endswith('.tar')
        return self._serial_wrapper.send(f"update backup {destination_tar_file}")
    
    def restore(self, restore_tar_file: str) -> str:
        assert restore_tar_file.endswith('.tar')
        return self._serial_wrapper.send(f"update restore {restore_tar_file}")