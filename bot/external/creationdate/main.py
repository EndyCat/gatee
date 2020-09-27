import json
import pathlib
import time
from typing import Callable, Tuple

import numpy as np
from numpy import ndarray


class CreationDate:
    def __init__(self, order: int = 3):
        self.order = order
        self.data_path = pathlib.Path.cwd().joinpath(
            "bot/external/creationdate/data/dates.json"
        )

        self.x, self.y = self._unpack_data()
        self._func = self._fit_data()

    def _unpack_data(self) -> Tuple[ndarray, ndarray]:
        with open(self.data_path) as string_data:
            data = json.load(string_data)

        x_data = np.array(list(map(int, data.keys())))
        y_data = np.array(list(data.values()))

        return x_data, y_data

    def _fit_data(self) -> Callable[[int], int]:
        fitted = np.polyfit(self.x, self.y, self.order)
        func = np.poly1d(fitted)

        return func

    def get_creation_date(self, tg_id: int) -> int:
        value = self._func(tg_id)
        current = time.time()

        if value > current:
            value = current  # type: ignore

        return value
