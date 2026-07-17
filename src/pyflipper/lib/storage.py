import re
import time


# TODO: Leverage pathlib to validate and manage file paths


class Storage:
    class Write:
        """Stream text/bytes into an interactive ``storage write`` session.

        ``storage write <file>`` puts the CLI into a listener that echoes every
        byte received into the file until it is broken out of with Ctrl-C.
        """

        def __init__(self, serial_wrapper) -> None:
            self._serial_wrapper = serial_wrapper

        def start(self, file: str) -> None:
            # Enter listener mode. We write the command directly (rather than
            # send()) because the listener never returns to the prompt.
            self._serial_wrapper.write(f"storage write {file}\r".encode())
            time.sleep(0.2)

        def send(self, text) -> None:
            if isinstance(text, str):
                text = text.encode("utf-8")
            self._serial_wrapper.write(bytes(text))

        def stop(self) -> str:
            # Break out of the listener, then drain back to the prompt.
            self._serial_wrapper.ctrl_c()
            time.sleep(0.2)
            return self._serial_wrapper.read_until_prompt()

        def file(self, text: str, path: str) -> None:
            self.start(path)
            self.send(text)
            # Give the bytes time to transmit + be written before Ctrl-C.
            # At 9600 baud that is ~960 B/s, so scale the wait with the size.
            time.sleep(max(0.5, len(text) / 900 + 0.3))
            self.stop()

    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
        self.write = Storage.Write(serial_wrapper=serial_wrapper)

    def info(self, fs: str) -> dict:
        assert fs in ('/ext', '/int'), "Storage filesystem must be '/ext' or '/int'"
        response = self._serial_wrapper.send(f"storage info {fs}")
        info_p = re.compile(r"(\w+):\s(.+)")
        info = info_p.findall(response)
        # Firmware has printed sizes as both "KB" and "KiB" over time.
        size_p = re.compile(r"(\d+)\s*Ki?B\s(\w+)")
        size = size_p.findall(response)
        result = {key: value.rstrip() for key, value in info}
        for amount, label in size:
            result[f"{label}_KB"] = int(amount)
        return result

    def format(self):
        # TODO: implement
        pass

    def _explorer(self, cmd: str, path: str) -> dict:
        dirs_p = re.compile(r"\[D\]\s(.+)")
        files_p = re.compile(r"\[F\]\s(.+)\s(\d+)(\w+)")
        response = self._serial_wrapper.send(f"storage {cmd} {path}")
        dirs = [d.strip() for d in dirs_p.findall(response)]
        files = [
            {'name': f[0].strip(), 'size': int(f[1]), 'weight': f[2]}
            for f in files_p.findall(response)
        ]
        return {'dirs': dirs, 'files': files}

    def list(self, path: str) -> dict:
        return self._explorer("list", path)

    def tree(self, path: str) -> dict:
        return self._explorer("tree", path)

    def remove(self, file: str) -> None:
        self._serial_wrapper.send(f"storage remove {file}")

    def read(self, file: str) -> str:
        response = self._serial_wrapper.send(f"storage read {file}")
        # The firmware prints a "Size: N" header line before the file content.
        lines = response.split('\r\n') if '\r\n' in response else response.split('\n')
        if lines and lines[0].startswith("Size:"):
            lines = lines[1:]
        return '\n'.join(lines).strip('\r\n')

    def copy(self, src: str, dest: str) -> None:
        self._serial_wrapper.send(f"storage copy {src} {dest}")

    def rename(self, file: str, new_file: str) -> None:
        self._serial_wrapper.send(f"storage rename {file} {new_file}")

    def mkdir(self, new_dir: str) -> None:
        self._serial_wrapper.send(f"storage mkdir {new_dir}")

    def md5(self, file: str) -> str:
        return self._serial_wrapper.send(f"storage md5 {file}")

    def stat(self, file: str) -> str:
        return self._serial_wrapper.send(f"storage stat {file}")
