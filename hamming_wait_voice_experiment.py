import requests
import os
import time
import logging
import sys
from dotenv import load_dotenv

from hamming_workflow.utils import get_experiment_url
from hamming_workflow.types import ExperimentStatus, ExperimentResult

load_dotenv()

logging.basicConfig(level=logging.INFO)


HAMMING_API_KEY = os.environ["HAMMING_API_KEY"]
AGENT_ID = os.environ["AGENT_ID"]
TIMEOUT_SECONDS = int(os.environ.get("TIMEOUT_SECONDS", 600))


def wait_for_experiment(experiment_id: str) -> str:
    url = f"https://app.hamming.ai/api/rest/voice-experiment/{experiment_id}"
    headers = {"Authorization": f"Bearer {HAMMING_API_KEY}"}

    start_time = time.time()

    while True:
        if time.time() - start_time > TIMEOUT_SECONDS:
            logging.error(f"Experiment timed out after {TIMEOUT_SECONDS} seconds")
            return "TIMEOUT"

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if ExperimentStatus(data["status"]) in [
            ExperimentStatus.FINISHED,
            ExperimentStatus.FAILED,
            ExperimentStatus.SCORING_FAILED,
        ]:
            return data["status"]
        else:
            logging.info(
                f"Waiting for experiment to complete. Experiment status: {data['status']}"
            )

        time.sleep(10)  # Wait for 10 seconds before polling again


def get_experiment_results(experiment_id: str) -> ExperimentResult:
    url = f"https://app.hamming.ai/api/rest/voice-experiment/{experiment_id}/calls"
    headers = {"Authorization": f"Bearer {HAMMING_API_KEY}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return ExperimentResult.model_validate(response.json())


if __name__ == "__main__":
    if HAMMING_API_KEY is None:
        raise ValueError("HAMMING_API_KEY is not set")
    if AGENT_ID is None:
        raise ValueError("AGENT_ID is not set")

    experiment_id = sys.argv[1]

    url = get_experiment_url(AGENT_ID, experiment_id)
    logging.info(
        f"Waiting for experiment to complete. Experiment ID: {experiment_id}. See url: {url}"
    )
    final_status = wait_for_experiment(experiment_id)
    logging.info(f"Experiment finished with status: {final_status}")

    if final_status == ExperimentStatus.FINISHED.value:
        logging.info("Fetching experiment results...")
        results = get_experiment_results(experiment_id)
        print(results.model_dump_json(indent=2))
    else:
        raise Exception(f"Experiment failed with status: {final_status}")
