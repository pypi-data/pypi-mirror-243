from collections.abc import Iterable
from typing import *
from ntt_signal import Signal


class ObservableList(list, Signal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        Signal.__init__(self, list)

        for ele in self:
            if isinstance(ele, Signal):
                ele.Attach(self)

    def append(self, __object: Any) -> None:
        r = super().append(__object)
        self.Emit(self)
        return r

    def pop(self, __index = -1) -> Any:
        r = super().pop(__index)
        self.Emit(self)
        return r

    def extend(self, __iterable: Iterable) -> None:
        r = super().extend(__iterable)
        self.Emit(self)
        return r

    def insert(self, __index, __object: Any) -> None:
        r = super().insert(__index, __object)
        self.Emit(self)
        return r

    def remove(self, __value: Any) -> None:
        r = super().remove(__value)
        self.Emit(self)
        return r

    def clear(self) -> None:
        r = super().clear()
        self.Emit(self)
        return r

    def reverse(self) -> None:
        r = super().reverse()
        self.Emit(self)
        return r

    def __setitem__(self, index, value) -> None:
        super().__setitem__(index, value)
        self.Emit(self)