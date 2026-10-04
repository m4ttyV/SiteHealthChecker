from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json
import time

import yaml

from database import Database
from logger import Logger
from monitor import Monitor

def read_config():
    with open('config.yaml', 'r') as config_file:
        sites = yaml.safe_load(config_file)
    return sites

def check(isDaemon: bool = False):
    logger = Logger()
    db = Database()
    if isDaemon:
        logger.info("Healthcheck daemon started")
    else: logger.info("Healthcheck started")

    sites = read_config()
    try:
        with ThreadPoolExecutor(max_workers=10) as executor:

            futures = [executor.submit(process_site, site) for site in sites['sites']]
            for future in as_completed(futures):
                result = future.result()
                if result["status"] == "OK":
                    logger.info(result["status_code"])
                else:
                    logger.error(result["status_code"])

                db.add_to_db(
                    result["site"],
                    result["status"],
                    result["status_code"],
                    result["response_time_ms"],
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )

    finally:
        if isDaemon:
            logger.info("Healthcheck iteration ended")
        else: logger.info("Healthcheck ended")

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


def daemon():
    logger = Logger()

    try:
        while True:
            try:
                check(True)
            finally:
                time.sleep(30)
    finally:
        logger.info("Healthcheck daemon ended")

def stats():
    db = Database()

    rows = db.check_count()
    data = db.read_from_db()

    for row in rows:
        print(f"""
        {row[0]}

        Всего проверок: {row[1]}
        Успешных: {row[2]}
        Неудачных: {row[3]}
        Среднее время: {row[4]} ms
        Последняя проверка: {row[5]}
        """)
    data = {
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "summary": rows,
        "checks": data
    }
    with open("./stats.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
