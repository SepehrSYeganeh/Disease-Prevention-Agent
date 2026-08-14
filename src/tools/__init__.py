import os
from .heartbeat_classifier import heartbeat_classifier

HB_CLASSIFIER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'ecgnet.pth'
)

__all__ = [
    "heartbeat_classifier"
]
