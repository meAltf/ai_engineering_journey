import logging
import os

def setup_logger(log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        filename = f"{log_dir}/app.log",
        level = logging.INFO,
        format = "%(asctime)s [%(levelname)s] %(message)s"
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger("").addHandler(console)

    return logging.getLogger("yt-transcriber")