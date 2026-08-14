import chainlit as cl
import torch
import torch.nn as nn
import json

from agents import AgentState
from . import HB_FORECASTER_PATH
from .utils import seq_beat2idx, seq_idx2beat


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


hb_forecaster_model = CharTransformer()
hb_forecaster_model.load_state_dict(torch.load(HB_FORECASTER_PATH, map_location=torch.device('cpu')))
hb_forecaster_model.eval()


async def heartbeat_forecaster(state: AgentState) -> AgentState:
    msg = cl.Message(content="heartbeat sequence forecaster...")
    await msg.send()

    # load data
    with open('../data/beat_symbols.json', encoding='utf-8') as file:
        beat_syms = json.load(file)
    data_id = '208'
    seq = seq_beat2idx(beat_syms[data_id])

    # forecast
    SEQ_LEN = CharTransformer.SEQ_LEN
    H = CharTransformer.H
    train_seq = seq[:-H]
    context = torch.tensor([train_seq[-SEQ_LEN:]])
    with torch.no_grad():
        logits = hb_forecaster_model(context)
        pred_idx = logits.argmax(dim=-1).squeeze(0)

    pred_char = seq_idx2beat(pred_idx.tolist())
    msg.content = f"heartbeat sequence: {pred_idx}"
    await msg.update()
    return {"hb_sequence": pred_char}
