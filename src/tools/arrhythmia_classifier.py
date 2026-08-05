import torch
import torch.nn as nn
import os


class ECGNet(nn.Module):

    def __init__(self):
        super(ECGNet, self).__init__()

        self.conv = nn.Sequential(
            nn.Conv1d(1, 32, kernel_size=7, padding=3),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.MaxPool1d(2),  # 186 -> 93

            nn.Conv1d(32, 64, kernel_size=5, padding=2),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(2),  # 93 -> 46

            nn.Conv1d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1)  # Global Average Pooling
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


def ecg_classifier(ecg):
    """
    classify an ecg as
    0 : Non-ecotic beats (normal beat)
    1 : Supraventricular ectopic beats
    2 : Ventricular ectopic beats*
    3 : Fusion Beats
    4 : Unknown Beats
    """
    x = torch.tensor(ecg, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
    print(x.shape)
    with torch.no_grad():
        pred = ecg_model(x).argmax(1).item()
        return pred


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'ecgnet.pth')
ecg_model = ECGNet()
ecg_model.load_state_dict(torch.load(model_path, map_location='cpu'))
ecg_model.eval()
