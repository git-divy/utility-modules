import subprocess
import threading


class MTCR:
    def __init__(self, cmds, callback):
        self.cmds = cmds
        self.callback = callback

    def __run_command(self, command: str):

        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
        except:
            raise Exception("Failed to create process")

        # Process Started
        if self.callback:
            while process.poll() is None:
                if process.stdout:
                    for line in process.stdout:
                        self.callback(
                            MTCR_Response(
                                pid=process.pid,
                                type="out",
                                command=command,
                                output=line.strip(),
                                return_code=process.returncode,
                            )
                        )

                if process.stderr:
                    for line in process.stderr:
                        self.callback(
                            MTCR_Response(
                                pid=process.pid,
                                type="err",
                                command=command,
                                output=line.strip(),
                                return_code=process.returncode,
                            )
                        )

            # Termination
            self.callback(
                MTCR_Response(
                    pid=process.pid,
                    type="trm",
                    command=command,
                    output=None,
                    return_code=process.returncode,
                )
            )

    def run(self):
        for cmd in self.cmds:
            threading.Thread(target=self.__run_command, args=(cmd,)).start()


class MTCR_Response:
    def __init__(self, pid, type, command, output, return_code):
        self.pid = pid
        self.type = type
        self.command = command
        self.output = output
        self.return_code = return_code

    def __str__(self) -> str:
        return str(self.__dict__)
