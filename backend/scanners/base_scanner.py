from __future__ import annotations

import time
import random
import statistics
from typing import Any
from urllib.parse import urljoin
from abc import ABC, abstractmethod

import requests

from config import settings
from schemas.test_result_schemas import TestResultCreate

class BaseScanner(ABC):
    """Abstract base class for all scanners."""

    def __init__(
        self,
        target_url: str,
        auth_token: str | None = None,
        max_requests: int | None = None,
    ):
        self.target_url = target_url.rstrip("/")
        self.auth_token = auth_token
        self.max_requests = max_requests or settings.DEFAULT_MAX_REQUESTS
        self.session = self._create_session()
        self.last_request_time = 0.0
        self.request_count = 0

    def _create_session(self) -> requests.Session:
        """Create persistent session with proper headers."""
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": f"{settings.APP_NAME}/{settings.VERSION}",
                "Accept": "application/json",
            }
        )

        if self.auth_token:
            session.headers.update({"Authorization": f"Bearer {self.auth_token}"})

        return session

    def _wait_before_request(self, jitter_ms: int | None = None) -> None:
        """Wait to respect the rate limit before making a request."""
        if jitter_ms is None:
            jitter_ms = settings.DEFAULT_JITTER_MS

        required_delay = 1.0 / (self.max_requests / settings.SCANNER_RATE_LIMIT_WINDOW_SECONDS)
        jitter = random.uniform(0, jitter_ms / 1000.0)

        elapsed_time = time.time() - self.last_request_time

        if elapsed_time < required_delay:
            time.sleep(required_delay - elapsed_time + jitter)
        else:
            time.sleep(jitter)

        self.last_request_time = time.time()


    def make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make a request with rate limiting and retry logic."""
        self._wait_before_request()

        url = urljoin(self.target_url, endpoint)
        retry_count = 0
        backoff_factor = 2.0

        kwargs.setdefault("timeout", settings.SCANNER_CONNECTION_TIMEOUT)

        while retry_count < settings.DEFAULT_RETRY_COUNT:
            try:
                start_time = time.time()
                response = self.session.request(method, url, **kwargs)
                setattr(response, "request_time", time.time() - start_time)

                self.request_count += 1

                if response.status_code == 429:  # Too Many Requests
                    retry_after = response.headers.get("Retry-After", str(settings.DEFAULT_RETRY_WAIT_SECONDS))
                    wait_time = int(retry_after) if retry_after.isdigit() else settings.DEFAULT_RETRY_WAIT_SECONDS
                    time.sleep(wait_time)
                    retry_count += 1
                    continue

                if response.status_code >= 500 and retry_count < settings.DEFAULT_RETRY_COUNT:  # Server errors
                    wait_time = backoff_factor ** retry_count
                    time.sleep(wait_time)
                    retry_count += 1
                    continue

                return response
            except (requests.Timeout, requests.ConnectionError):
                if retry_count < settings.DEFAULT_RETRY_COUNT:
                    wait_time = backoff_factor ** retry_count
                    time.sleep(wait_time)
                    retry_count += 1
                    continue
                else:
                    raise
        return response

    @abstractmethod
    def scan(self) -> TestResultCreate:
        """Perform the scan and return a TestResultCreate object."""