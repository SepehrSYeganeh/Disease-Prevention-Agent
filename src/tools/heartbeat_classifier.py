import chainlit as cl
import torch
import torch.nn as nn
import pandas as pd

from agents.config import AgentState
from .config import HB_CLASSIFIER_PATH, CLASSIFIER_DATA_PATH
from .utils import hb_int2char


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


hb_classifier_model = HBClassifierNet()
hb_classifier_model.load_state_dict(torch.load(HB_CLASSIFIER_PATH, map_location=torch.device('cpu')))
hb_classifier_model.eval()


async def hb_classifier(state: AgentState) -> AgentState:
    msg = cl.Message(content="heartbeat classifier...")
    await msg.send()

    # pick a random heartbeat ECG sample
    df = pd.read_csv(CLASSIFIER_DATA_PATH)
    ecg = df.sample(n=1).iloc[0, :186].to_numpy()

    # classify
    x = torch.tensor(ecg, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
    with torch.no_grad():
        pred = hb_classifier_model(x).argmax(1).item()

    pred_char = hb_int2char(pred)
    msg.content = f"heartbeat class: {pred_char}"
    await msg.update()
    return {'hb_class': pred_char}
