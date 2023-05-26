
class Loader:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
    
    def list(self) -> dict:
        response = self._serial_wrapper.send("loader list")
        result = {}
        current_category = ""

        for line in response.split('\n'):
            if ':' in line:
                current_category = line[:-2]
                result[current_category] = []
            else:
                value = line.strip()
                if value:
                    result[current_category].append(value)
                    
        return {x: y for x, y in result.items() if x or y}
    
    def open(self, app_name: str) -> None:
        self._serial_wrapper.send(f"loader open {app_name}")