import os
from pathlib import Path

_ROOT_DIR = Path(__file__).resolve().parents[2]

CLASSIFIER_DATA_PATH = _ROOT_DIR / "data" / "mitbih_test.csv"
FORECASTER_DATA_PATH = _ROOT_DIR / "data" / "beat_symbols.json"

HB_CLASSIFIER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'hb_classifier_model.pth'
)


HB_FORECASTER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'hb_forecaster_model.pth'
)
