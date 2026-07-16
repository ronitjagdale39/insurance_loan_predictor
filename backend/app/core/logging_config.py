import os
import logging

logger = logging.getLogger("insurance_app")

logger.setLevel(logging.INFO)

# Make the log path absolute relative to this config file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.normpath(os.path.join(current_dir, "..", "logs", "app.log"))
file_handler = logging.FileHandler(log_path)

console_handler = logging.StreamHandler()

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(formatter)

console_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.addHandler(console_handler)