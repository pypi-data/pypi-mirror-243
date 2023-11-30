# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Author:       yunhgu
# Date:         2023/8/3
# -------------------------------------------------------------------------------
from pathlib import Path

import cv2
import numpy as np

from .base import IO


class Img(IO):
    @classmethod
    def read(cls, path, flags=1) -> dict:
        """read img

        Args:
            path: img path
            flags: flags 0 1 2. Defaults to 1.

        Returns:
            _description_
        """
        return cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), flags)

    @classmethod
    def write(cls, path, img_array):
        cv2.imencode(Path(path).suffix, img_array)[1].tofile(str(path))

    @staticmethod
    def name():
        """
        :return: string with name of geometry
        """
        return "image"
