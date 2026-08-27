import yaml
import os

from logger import setup_logger
from downloader import download_audio, split_audio
from transcriber import load_model, transcribe_chunks, save_json
from utils import extract_video_id


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

    logger.info(f"Processing {len(urls)} videos")

    for i, url in enumerate(urls, 1):
        try:
            logger.info(f"[{i}] Processing: {url}")

            # clean playlist part
            clean_url = url.split("&list=")[0]

            video_id = extract_video_id(clean_url)

            # Step 1: Download
            audio_path = download_audio(clean_url, config["paths"]["audio_dir"])

            # Step 2: Split
            chunk_dir = f"chunks/{video_id}"
            chunks = split_audio(audio_path, chunk_dir)

            # Step 3: Transcribe
            results = transcribe_chunks(model, chunks, video_id)

            # Step 4: Save JSON
            output_file = os.path.join(
                config["paths"]["output_dir"],
                f"{video_id}.json"
            )

            save_json(results, output_file)

            logger.info(f"Done: {video_id}")

        except Exception as e:
            logger.error(f"Failed for {url}: {str(e)}")

    logger.info("All videos processed!")


if __name__ == "__main__":
    main()