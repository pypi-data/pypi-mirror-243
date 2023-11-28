#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : types
# @Time         : 2023/8/15 12:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
from os import PathLike

from meutils.pipe import *

StrPath = Union[str, PathLike]
StrOrPath = Union[str, PathLike]
StrOrCallableStr = Union[str, Callable[..., str]]

from typing import List


def is_list_of_strings(lst):
    return isinstance(lst, List) and all(isinstance(item, str) for item in lst)


def is_list_of_ints(lst):
    return isinstance(lst, List) and all(isinstance(item, int) for item in lst)
