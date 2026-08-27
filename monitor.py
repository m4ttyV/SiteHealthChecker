import requests
import time
from dataclasses import dataclass

@dataclass
class Response:
    status_code: int
    response_time_ms: float

class Monitor:
    def health_check(self, url: str):
        start = time.time()
        try:
            response = requests.get(url, timeout=5)
            response_code = response.status_code
        except requests.exceptions.RequestException as e:
            print(e)
            response_code = 504
        end = time.time()
        return Response(status_code=response_code, response_time_ms=int((end - start) * 1000))
