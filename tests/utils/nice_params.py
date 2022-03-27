from typing import Any

import pytest


class NiceParam:
    def __init__(
        self, param, id: str | None = None, marks: Any = ()
    ):  # pylint: disable=redefined-builtin
        self.id = id
        self.marks = marks
        self.param = param


def nice_param(*args, **kwargs) -> NiceParam:
    return NiceParam(*args, **kwargs)


def nice_parametrize(*params: dict | NiceParam):
    names = []
    values = []

    for param in params:
        param_dict: dict
        if isinstance(param, NiceParam):
            param_dict = param.param
        else:
            param_dict = param
        for key in param_dict:
            if key not in names:
                names.append(key)

    for param in params:
        if isinstance(param, NiceParam):
            value = pytest.param(
                *(param.param.get(name, None) for name in names),
                id=param.id,
                marks=param.marks
            )
        else:
            value = tuple(param.get(name, None) for name in names)
        values.append(value)

    return pytest.mark.parametrize(names, values)
