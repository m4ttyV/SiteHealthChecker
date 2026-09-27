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

    def info(self, message):
        self.log(message, 'INFO')

    def error(self, message):
        self.log(message, 'ERROR')