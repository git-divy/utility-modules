import subprocess
import threading
import shlex


class MTCR:
    def __init__(self, cmds, callback):
        self.cmds = cmds
        self.callback = callback

    def __stream_output(self, stream, pid, command, out_type):
        try:
            for line in iter(stream.readline, ""):
                self.callback(
                    {
                        "pid": pid,
                        "type": out_type,
                        "command": command,
                        "output": line.rstrip("\n"),
                        "return_code": None,
                    }
                )
        except Exception as e:
            self.callback(
                {
                    "pid": pid,
                    "type": "err",
                    "command": command,
                    "output": f"[Stream error: {e}]",
                    "return_code": None,
                }
            )
        finally:
            stream.close()

    def __run_command(self, command):
        if isinstance(command, str):
            cmd_list = shlex.split(command)
        else:
            cmd_list = command

        try:
            process = subprocess.Popen(
                cmd_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
        except Exception as e:
            self.callback(
                {
                    "pid": None,
                    "type": "err",
                    "command": command,
                    "output": f"[Launch failed: {e}]",
                    "return_code": None,
                }
            )
            return

        # Stream both stdout and stderr
        for out_type, stream in [("out", process.stdout), ("err", process.stderr)]:
            threading.Thread(
                target=self.__stream_output,
                args=(stream, process.pid, command, out_type),
                daemon=True,
            ).start()

        process.wait()
        self.callback(
            {
                "pid": process.pid,
                "type": "trm",
                "command": command,
                "output": None,
                "return_code": process.returncode,
            }
        )

    def run(self):
        threads = [
            threading.Thread(target=self.__run_command, args=(cmd,))
            for cmd in self.cmds
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()


if __name__ == "__main__":
    MTCR(["ls", "ls", "dir", "yt-dlp", "ipconfig"], lambda x: print(x)).run()
