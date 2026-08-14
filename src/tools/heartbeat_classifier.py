import torch
import torch.nn as nn
import pandas as pd

from . import HB_CLASSIFIER_PATH
from agents import AgentState


class HBClassifierNet(nn.Module):

    def __init__(self):
        super().__init__()

        self.conv = nn.Sequential(
            nn.Conv1d(1, 32, kernel_size=7, padding=3),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.MaxPool1d(2),

            nn.Conv1d(32, 64, kernel_size=5, padding=2),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(2),

            nn.Conv1d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1)
        )

        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 5)
        )

    def forward(self, x):
        x = self.conv(x)
        return self.fc(x)


def hb_char2int(hb_char: str) -> int:
    mapping = {
        'N': 0,  # Non-ectopic beats
        'S': 1,  # Supraventricular ectopic beats
        'V': 2,  # Ventricular ectopic beats
        'F': 3,  # Fusion Beats
        'Q': 4  # Unknown Beats
    }
    try:
        return mapping[hb_char.upper()]
    except KeyError:
        raise ValueError(f"Invalid heartbeat character: '{hb_char}'. "
                         f"Expected one of {list(mapping.keys())}")


def hb_int2char(hb_int: int) -> str:
    mapping = {
        0: 'N',  # Non-ectopic beats
        1: 'S',  # Supraventricular ectopic beats
        2: 'V',  # Ventricular ectopic beats
        3: 'F',  # Fusion Beats
        4: 'Q'  # Unknown Beats
    }
    try:
        return mapping[hb_int]
    except KeyError:
        raise ValueError(f"Invalid heartbeat integer: '{hb_int}'. "
                         f"Expected one of {list(inverse_mapping.keys())}")


hb_classifier_model = HBClassifierNet()
hb_classifier_model.load_state_dict(torch.load(HB_CLASSIFIER_PATH, map_location='cpu'))
hb_classifier_model.eval()


async def heartbeat_classifier(state: AgentState) -> AgentState:
    df = pd.read_csv("../data/mitbih_test.csv")
    ecg = df.sample(n=1).iloc[0, :186].to_numpy()  # pick a random row
    x = torch.tensor(ecg, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
    with torch.no_grad():
        pred = hb_classifier_model(x).argmax(1).item()
        pred_char = hb_int2char(pred)
        return {'hb_char': pred_char}
