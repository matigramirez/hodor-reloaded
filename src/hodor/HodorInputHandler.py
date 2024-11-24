import threading
import select
import sys
from queue import Queue, Empty


class HodorInputHandler:
    def __init__(self):
        self.running = True
        self.command_queue = Queue()

        # Ejecutar el handler en otro thread
        self.input_thread = threading.Thread(target=self.__input_handler__)
        self.input_thread.daemon = True
        self.input_thread.start()

    def __input_handler__(self):
        while self.running:
            if select.select([sys.stdin], [], [], 0.1)[0]:
                try:
                    command = sys.stdin.readline().strip()

                    if command:
                        self.command_queue.put(command)

                except (IOError, EOFError):
                    # Handle SSH disconnection gracefully
                    self.running = False
                    break

    def get_next_command(self):
        try:
            return self.command_queue.get_nowait()
        except Empty:
            return None

    def close(self):
        self.running = False
