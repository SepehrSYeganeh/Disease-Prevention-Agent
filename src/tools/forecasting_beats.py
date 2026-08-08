import torch
import torch.nn as nn


def beat_to_idx(symbols: list[str]) -> list[int]:
    aami_mapping = {
        # class N
        'N': 0, 'L': 0, 'R': 0, 'e': 0, 'j': 0,
        # class S
        'S': 1, 'A': 1, 'a': 1, 'J': 1,
        # class V
        'V': 2, 'E': 2,
        # class F
        'F': 3
    }
    return [aami_mapping.get(sym, 4) for sym in symbols]


def calc_weights(seq: list[int]):
    N = len(seq)
    counts = pd.Series(seq).value_counts()
    K = len(counts)
    weights = N / (K * counts)
    weights = torch.tensor([weights.get(i, 0) for i in range(CharTransformer.V)], dtype=torch.float)
    return weights / weights.mean()


class CharTransformer(nn.Module):
    SEQ_LEN: int = 200  # context window
    H: int = 20  # horizon
    V: int = 5  # vocab size

    def __init__(
            self,
            d_model: int = 64,
            nhead: int = 4,
            num_layers: int = 2
    ):
        super().__init__()

        self.embed = nn.Embedding(self.V, d_model)
        self.pos = nn.Embedding(self.SEQ_LEN, d_model)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=128,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers)

        self.head = nn.Linear(d_model, self.H * self.V)

    def forward(self, x):
        B, T = x.shape
        pos = torch.arange(T, device=x.device)
        out = self.embed(x) + self.pos(pos)
        out = self.transformer(out)

        last = out[:, -1, :]
        logits = self.head(last)
        logits = logits.view(B, self.H, -1)
        return logits
