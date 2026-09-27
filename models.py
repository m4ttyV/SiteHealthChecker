from database import Database
from logger import ErrorLogger, InfoLogger
from monitor import Monitor, Response
from datetime import datetime
import yaml
import time
import atexit
import json

def read_config():
    with open('config.yaml', 'r') as config_file:
        sites = yaml.safe_load(config_file)
    return sites

def check():
    info_logger = InfoLogger()
    error_logger = ErrorLogger()
    monitor = Monitor()
    db = Database()

    info_logger.log_info("Healthcheck started")
    sites = read_config()
    try:
        for site in sites['sites']:
            site = site.strip()
            response = monitor.health_check(site)
            status = "OK" if response.status_code == 200 else "ERROR"
            if status == "OK":
                info_logger.log_info(response.status_code)
            else:
                error_logger.log_error(response.status_code)

            db.add_to_db(
                site,
                status,
                response.status_code,
                response.response_time_ms,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
    finally:
        info_logger.log_info("Healthcheck ended")

def process_site(site: str):
    monitor = Monitor()

    site = site.strip()
    response = monitor.health_check(site)

    return {
        "site": site,
        "status": "OK" if response.status_code == 200 else "ERROR",
        "status_code": response.status_code,
        "response_time_ms": response.response_time_ms
    }


def deamon():
    info_logger = InfoLogger()
    error_logger = ErrorLogger()
    monitor = Monitor()
    db = Database()
    try:
        while True:
            info_logger.log_info("Healthcheck daemon started")
            sites = read_config()
            try:
                for site in sites['sites']:
                    site = site.strip()
                    response = monitor.health_check(site)
                    if response.status_code == 200:
                        info_logger.log_info(response.status_code)
                        db.add_to_db(site, "OK", response.status_code, response.response_time_ms,
                                     datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        error_logger.log_error(response.status_code)
                        db.add_to_db(site, "ERROR", response.status_code, response.response_time_ms,
                                     datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            finally:
                info_logger.log_info("Healthcheck iteration ended")
                time.sleep(30)
    finally:
        info_logger.log_info("Healthcheck daemon ended")

def stats():
    db = Database()

    rows = db.check_count()
    data = db.read_from_db()

    for row in rows:
        print(f"""
            {row['url']}
            Всего проверок: {row['total_checks']}
            Успешных: {row['success_checks']}
            Неудачных: {row['failed_checks']}
            Среднее время: {row['avg_response_ms']} ms
            Последняя проверка: {row['last_check']}
            """)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("./stats.txt", "a") as file:
        file.write(f"Stats was created by: {timestamp}\n")
        file.write(f"{json.dumps(data, indent=4, ensure_ascii=False)}\n")
