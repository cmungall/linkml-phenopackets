import os
from pathlib import Path

THIS_PATH = Path(__file__).parent
INPUT_PATH = THIS_PATH / "input"
OUTPUT_PATH = THIS_PATH / "output"
INPUT_EXAMPLES_PATH = THIS_PATH / "input" / "examples"
OUTPUT_EXAMPLES_PATH = THIS_PATH / "output" / "examples"

RESOURCE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "input")
TARGET_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "target")
JSONLD_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../jsonld")
