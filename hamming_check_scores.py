import json
import sys
import logging

from hamming_workflow.utils import get_experiment_url
from hamming_workflow.types import ExperimentResult

logging.basicConfig(level=logging.INFO)




def check_scores(data: ExperimentResult) -> bool:
    for call in data.calls:
        if call.status != "ended":
            logging.error(f"Error: Call {call.id} has status {call.status}, expected 'ended'")
            return False

        for score_id, score in call.scores.items():
            if score.value == 0:
                logging.error(
                    f"Error: Call {call.id} has score 0 for scoring function {score_id}"
                )
                return False

    return True


if __name__ == "__main__":
    input_data = json.load(sys.stdin)

    try:
        experiment_result = ExperimentResult.model_validate(input_data)
    except ValueError as e:
        logging.error(f"Error parsing input data: {e}")
        sys.exit(1)

    if check_scores(experiment_result):
        logging.info("All checks passed successfully.")
        sys.exit(0)
    else:
        logging.error("Checks failed.")
        sys.exit(1)
