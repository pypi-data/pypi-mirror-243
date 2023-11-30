import os
import time

import replicate

from replicate_whisper_diarization.logger import get_logger

logger = get_logger(__name__)

MODEL_NAME = os.getenv("WHISPER_MODEL_NAME", "collectiveai-team/whisper-wordtimestamps")
MODEL_VERSION = os.getenv(
    "WHISPER_MODEL_VERSION",
    "f1b798d0e65d792312d0fca9f43311e390cc86de96da12243760687d660281f4",
)

model = replicate.models.get(MODEL_NAME)
version = model.versions.get(MODEL_VERSION)


def transcribe(
    audio_url: str,
    audio_file: str | None = None,
    model: str = "base",
    webhook_url: str | None = None,
) -> dict:
    replicate_input = {"audio_url": audio_url, "model": model, "word_timestamps": True}
    if audio_file:
        replicate_input = {"audio": audio_file, "model": model, "word_timestamps": True}
    if webhook_url:
        prediction = replicate.predictions.create(
            version=version,
            input=replicate_input,
            webhook=webhook_url,
        )
    else:
        prediction = replicate.predictions.create(
            version=version,
            input=replicate_input,
        )

    while prediction.status not in ["failed", "succeeded"] and not webhook_url:
        time.sleep(5)
        prediction.reload()
    if prediction.status == "failed":
        logger.error("Transcription failed")
    output = prediction.output
    return output
