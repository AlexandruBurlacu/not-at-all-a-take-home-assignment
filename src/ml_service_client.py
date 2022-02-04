from typing import Iterable
from .storage import fetch_blogpost, update_blogpost
from .mocked_requests import AbstractRequester

from concurrent.futures import ThreadPoolExecutor
import time
import random
import os
import logging


MAX_CONURRENT_TASKS = int(os.environ.get("MAX_CONURRENT_TASKS", "8"))
executor = ThreadPoolExecutor(max_workers=MAX_CONURRENT_TASKS)

_sleep = time.sleep

def backoff_timeout(retry: int):
    return 0.3 * 2 ** retry + 0.1 * random.randint(5, 15)


class FoulLanguageDetector:
    def __init__(self, requester: AbstractRequester):
        self.requester = requester

    def detect_foul_language(self, blogpost_id: str) -> None:
        executor.submit(self.detect_foul_language_task, blogpost_id)

    def detect_foul_language_task(self, blogpost_id: str):
        blogpost = fetch_blogpost(blogpost_id)
        
        paragraph_predictions: Iterable[bool | None] = executor.map(self.predict_foul_language, blogpost.paragraphs)

        if any(paragraph_predictions):
            update_blogpost(blogpost_id, has_foul_language=True)
        else:
            update_blogpost(blogpost_id, has_foul_language=False)

    def predict_foul_language(self, blogpost_paragraph: str) -> bool | None:

        response = self.requester.post("https://internal-api.example.com/v0/sentences", headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer some_dummy_token"
        }, json={"fragment": blogpost_paragraph})

        for retry in range(5):
            if response.status_code >= 500:
                logging.warning(f"Received a 5xx status code, retrying [{retry+1}/5]")

                backoff_seconds = backoff_timeout(retry)
                _sleep(backoff_seconds)

                response = self.requester.post("https://internal-api.example.com/v0/sentences", headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer some_dummy_token"
                }, json={"fragment": blogpost_paragraph})

        return response.json().get("hasFoulLanguage") # type: ignore

