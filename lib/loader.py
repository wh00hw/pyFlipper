from urllib import response


class Loader:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
    
    def list(self):
        response = self._serial_wrapper.send("loader list")
        result = {}
        current_category = ""
        for e in response.split('\n'):
            if ':' in e:
                current_category = e[:-2]
                result[current_category] = []
                continue
            result[current_category].append(e.strip())
        return result
    
    def open(self, app_name):
        return self._serial_wrapper.send(f"loader open {app_name}")