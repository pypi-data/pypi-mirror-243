from time import sleep, time


class RateLimiter:
    def __init__(self, min_wait_time_in_sec: int = 1) -> None:
        self.min_wait_time_in_sec: int = min_wait_time_in_sec
        self.last_call: float = time() - min_wait_time_in_sec

    def wait(self) -> None:
        if time() - self.last_call < self.min_wait_time_in_sec:
            sleep(min(1, time() - self.last_call))
        self.last_call = time()
