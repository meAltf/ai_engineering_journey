import yaml
import os
from logger import setup_logger
from downloader import download_audio
from transcriber import load_model, transcribe
from utils import save_text


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()
    logger = setup_logger(config["paths"]["log_dir"])

    model = load_model(
        config["model"],
        config["compute_type"]
    )

    urls = config["youtube"]["urls"]

    logger.info(f"Starting batch processing: {len(urls)} videos")

    for i, url in enumerate(urls, 1):
        try:
            logger.info(f"[{i}] Processing: {url}")

            audio_path = download_audio(url, config["paths"]["audio_dir"])
            text = transcribe(model, audio_path)

            filename = f"video_{i}"
            saved_path = save_text(text, config["paths"]["output_dir"], filename)

            logger.info(f"Saved: {saved_path}")

        except Exception as e:
            logger.error(f"Failed for {url}: {str(e)}")

    logger.info("Batch processing completed")