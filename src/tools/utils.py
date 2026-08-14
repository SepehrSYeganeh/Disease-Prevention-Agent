def hb_char2int(hb_char: str) -> int:
    mapping = {
        'N': 0,  # Non-ectopic beats
        'S': 1,  # Supraventricular ectopic beats
        'V': 2,  # Ventricular ectopic beats
        'F': 3,  # Fusion Beats
        'Q': 4  # Unknown Beats
    }
    return mapping.get(hb_char.upper(), 4)


def hb_int2char(hb_int: int) -> str:
    mapping = {
        0: 'N',  # Non-ectopic beats
        1: 'S',  # Supraventricular ectopic beats
        2: 'V',  # Ventricular ectopic beats
        3: 'F',  # Fusion Beats
        4: 'Q'  # Unknown Beats
    }
    return mapping.get(hb_int, 'Q')


def seq_beat2idx(symbols: list[str]) -> list[int]:
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


def seq_idx2beat(indices: list[int]) -> list[str]:
    mapping = {
        0: 'N',  # Non-ectopic beats
        1: 'S',  # Supraventricular ectopic beats
        2: 'V',  # Ventricular ectopic beats
        3: 'F',  # Fusion Beats
        4: 'Q'  # Unknown Beats
    }
    return "".join([mapping.get(idx, 'Q') for idx in indices])
