from itertools import islice
from typing import Dict, Iterator, List, Optional, Tuple

from ..enums import Punishment, ViolationType


def sort_punishments_by_weight(
    chat_settings, ignore_none_punishments: bool = True
) -> List[Punishment]:
    punishments: Dict[str, int] = {}

    for violation_type in [
        ViolationType.InappropriateAccountCreationDate,
        ViolationType.URLInName,
        ViolationType.SpamWatchBan,
        ViolationType.RTLCharactersInName,
        ViolationType.CasBanned,
    ]:
        punishment: Optional[int] = chat_settings[violation_type.value].type
        if punishment is not None or not ignore_none_punishments:
            punishments[violation_type.name] = punishment

    sorted_keys = sorted(
        punishments.keys(), key=lambda k: (punishments[k] is None, punishments[k])
    )
    sorted_punishments = {x: punishments[x] for x in sorted_keys}

    return [
        Punishment(type=type_, name=name) for name, type_ in sorted_punishments.items()
    ]


def chunks(lst: List, n: int) -> Iterator:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def dict_chunks(dct: Dict, n: int) -> Iterator:
    it = iter(dct)
    for _ in range(0, len(dct), n):
        yield {k: dct[k] for k in islice(it, n)}


def interpolate(
    f_co: Tuple[int, int, int], t_co: Tuple[int, int, int], interval: int
) -> Iterator:
    det_co = [(t - f) / interval for f, t in zip(f_co, t_co)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(f_co, det_co)]
