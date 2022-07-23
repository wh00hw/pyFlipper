import re

class Storage:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
    
    def error_handler(self, response):
        pattern = re.compile("Storage error:\s.*")
        error_msg = pattern.match(response)
        if error_msg:
            raise Exception(error_msg)

    def info(self, path):
        info_p = re.compile("(\w+):\s(.+)")
        response = self._serial_wrapper.send(f"storage info {path}")
        info = info_p.findall(response)
        size_p = re.compile("(\d+)KB\s(\w+)")
        size = size_p.findall(response)
        return { info[0][0]: info[0][1].rstrip(), info[1][0]: info[1][1].rstrip(), size[0][1]+"_KB": int(size[0][0]), size[1][1]+"_KB": int(size[1][0])}
    
    def format(self, path):
        pass

    def _explorer(self, cmd, path):
        dirs_p = re.compile("\[D\]\s(\w+)")
        files_p = re.compile("\[F\]\s(.+)\s(\d+)(\w+)")
        response = self._serial_wrapper.send(f"storage {cmd} {path}")
        dirs = dirs_p.findall(response)
        self.error_handler(response)
        files = [{'name': file[0], 'size': int(file[1]), 'weight': file[2]} for file in files_p.findall(response)]
        return {'dirs': dirs, 'files': files}

    def list(self, path):
        return self._explorer("list", path)
    
    def tree(self, path):
        return self._explorer("tree", path)
    
    def remove(self):
        pass

