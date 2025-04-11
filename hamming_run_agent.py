import requests
import os
from dotenv import load_dotenv
import logging
from hamming_workflow.utils import get_experiment_url

load_dotenv()

logging.basicConfig(level=logging.INFO)

HAMMING_API_KEY = os.environ["HAMMING_API_KEY"]

AGENT_ID = os.environ["AGENT_ID"]
DATASET_ID = os.environ["DATASET_ID"]
TO_NUMBERS = os.environ.get("TO_NUMBERS", os.environ.get("TO_NUMBER"))


def run_agent(agent_id: str, dataset_id: str) -> str:
    url = f"https://app.hamming.ai/api/rest/voice-agent/{agent_id}/run"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HAMMING_API_KEY}",
    }
    
    to_number = TO_NUMBERS.split(",") if "," in TO_NUMBERS else TO_NUMBERS
    
    data = {"dataset_id": dataset_id, "to_number": to_number}

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    data = response.json()

    if "voice_experiment_id" not in data:
        raise Exception(f"Invalid response from Hamming API: {data}")

    voice_experiment_id = data["voice_experiment_id"]
    url = get_experiment_url(agent_id, voice_experiment_id)
    logging.info(
        f"Started experiment {voice_experiment_id} for agent {agent_id}. See url for more details: {url}"
    )

    return voice_experiment_id


if __name__ == "__main__":
    if HAMMING_API_KEY is None:
        raise ValueError("HAMMING_API_KEY is not set")
    if AGENT_ID is None:
        raise ValueError("AGENT_ID is not set")
    if DATASET_ID is None:
        raise ValueError("DATASET_ID is not set")
    if TO_NUMBERS is None:
        raise ValueError("Neither TO_NUMBERS nor TO_NUMBER is set")
    experiment_id = run_agent(AGENT_ID, DATASET_ID)
    print(experiment_id)
