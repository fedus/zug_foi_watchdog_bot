import os
import sys
from pathlib import Path

from dotenv import dotenv_values

is_dev = "--dev" in sys.argv or os.environ.get("ENV", "PROD") == "DEV"
dotenv_variant = "dev" if is_dev else "prod"

base_path = Path(os.environ.get('CONFIG_DIR', '.'))

config = {
    **dotenv_values(f"{base_path}/.secrets.base.env"),
    **dotenv_values(f"{base_path}/.shared.base.env"),
    **dotenv_values(f"{base_path}/.secrets.{dotenv_variant}.env"),
    **dotenv_values(f"{base_path}/.shared.{dotenv_variant}.env"),
    **os.environ,
    "DEV": is_dev,
}
