import os
from datetime import datetime


class Logger:
    def __init__(self, filename="./logs/logs.txt"):
        self.filename = filename

        log_dir = os.path.dirname(filename)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_text = f"{level} - [{timestamp}] {message}"

        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(f"{log_text}\n")

        print(log_text)

    def info(self, message):
        self.log(message, "INFO")

    def error(self, message):
        self.log(message, "ERROR")
