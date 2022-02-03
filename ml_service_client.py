from charset_normalizer import logging
from storage import fetch_blogpost, update_blogpost
from mocked_requests import AbstractRequester

from concurrent.futures import ThreadPoolExecutor
import time
import random
import os


MAX_CONURRENT_TASKS = int(os.environ.get("MAX_CONURRENT_TASKS", "8"))
executor = ThreadPoolExecutor(max_workers=MAX_CONURRENT_TASKS)


def backoff_timeout(retry: int):
    backoff_seconds = 0.3 * 2 ** retry + 0.1 * random.randint(5, 15)
    time.sleep(backoff_seconds)


class FoulLanguageDetector:
    def __init__(self, requester: AbstractRequester):
        self.requester = requester

    def detect_foul_language(self, blogpost_id: str) -> None:
        executor.submit(self._detect_foul_language_task, blogpost_id)

    def _detect_foul_language_task(self, blogpost_id: str):
        blogpost = fetch_blogpost(blogpost_id)
        
        futures = executor.map(self._predict_foul_language, blogpost.paragraphs)

        if any(future.result for future in futures):
            update_blogpost(blogpost_id, has_foul_language=True)
        else:
            update_blogpost(blogpost_id, has_foul_language=False)

    def _predict_foul_language(self, blogpost_paragraph: str):

        response = self.requester.post("https://internal-api.example.com/v0/sentences", headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer some_dummy_token"
        }, json={"fragment": blogpost_paragraph})

        for retry in range(5):
            if response.status_code >= 500:
                logging.warning(f"Received a 5xx status code, retrying [{retry+1}/5]")

                backoff_timeout(retry)

                response = self.requester.post("https://internal-api.example.com/v0/sentences", headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer some_dummy_token"
                }, json={"fragment": blogpost_paragraph})
        
        return response.json().get("hasFoulLanguage")

