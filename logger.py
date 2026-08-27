# ### 4. Логирование
#
# Создать файл:
#
# ```text
# logs/app.log
# ```
#
# Логировать:
#
# ```text
# INFO  - начало проверки
# INFO  - успешная проверка
# ERROR - ошибка подключения
# ```
from datetime import datetime


class Logger:
    def __init__(self, filename='./logs/logs.txt'):
        self.filename = filename

    def log(self, message, level='INFO'):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_text = f'{level} - [{timestamp}] {message}'
        with open(self.filename, "a") as file:
            file.write(f"{log_text}\n")
        print(log_text.strip())

class ErrorLogger(Logger):
    def log_error(self, message):
        self.log(message, level='ERROR')

class InfoLogger(Logger):
    def log_info(self, message):
        self.log(message, level='INFO')