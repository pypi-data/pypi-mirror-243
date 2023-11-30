# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Author:       yunhgu
# Date:         2023-10-27 16:40:37
# @Copyright:  www.shujiajia.com  Inc. All rights reserved.
# Description: 注意：本内容仅限于数据堂公司内部传阅，禁止外泄以及用于其他的商业目的
# -------------------------------------------------------------------------------
from rich.console import Console
from rich.table import Table
import numpy as np

console = Console()
table = Table(header_style="bold blue", show_lines=True)


def PrintTable(info):
    """print table

    Args:
        info: [
                [title1,title2,...],
                [value1,value2,...],
                [...]
            ]
    """
    max_char_width = max(list(map(lambda value: len(value), np.array(info, dtype=str).flatten().tolist())))
    for title in info[0]:
        table.add_column(f"{title}", width=max_char_width)
    for values in info[1:]:
        table.add_row(*[f"{v}" for v in values], style="green")
    console.print(table)
