import os
import time

import replicate

from replicate_whisper_diarization.logger import get_logger
from replicate_whisper_diarization.diarization.utils import (
    language_mapping,
    convert_to_miliseconds,
    get_words_speaker_mapping,
    get_sentences_speaker_mapping,
)

logger = get_logger(__name__)

MODEL_NAME = os.getenv(
    "DIARIZATION_MODEL_NAME",
    "collectiveai-team/speaker-diarization-3",
)
MODEL_VERSION = os.getenv(
    "DIARIZATION_MODEL_VERSION",
    "f7425066750cd06fdf95b831c08bba1530f222a2eb4145f40493f431b7483b95",
)


def parse_diarization_segments(segments: list[dict]) -> list:
    speaker_ts = []
    for segment in segments:
        speaker_ts.append(
            [
                convert_to_miliseconds(segment["start"]),
                convert_to_miliseconds(segment["stop"]),
                segment["speaker"],
            ]
        )
    return speaker_ts


def run_segmentation(audio_url: str) -> list[dict]:
    model = replicate.models.get(MODEL_NAME)
    version = model.versions.get(MODEL_VERSION)

    prediction = replicate.predictions.create(
        version=version,
        input={"audio": audio_url},
    )

    while prediction.status not in ["failed", "succeeded"]:
        time.sleep(5)
        prediction.reload()
    if prediction.status == "failed":
        logger.error("Diarization failed")
    output = prediction.output
    # url = prediction.output
    # response = requests.get(url)

    # if response.status_code == 200:
    #     output = json.loads(response.content)
    # data is now a dictionary containing the JSON content
    # else:
    #     raise Exception("Diarization failed")
    segements = output["segments"]
    return segements


def run_diarization(
    audio_url: str, word_timestamps: list[dict[str, float]], language: str
):
    language = language_mapping.get(language, "en")
    segements = run_segmentation(audio_url)
    segements = parse_diarization_segments(segements)
    wsm = get_words_speaker_mapping(word_timestamps, segements, "start")
    ssm = get_sentences_speaker_mapping(wsm, segements)
    return ssm
