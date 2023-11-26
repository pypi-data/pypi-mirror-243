# Copyright (c) 2012-2023 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

__all__ = ('Signal',)


class Signal:

    def __init__(self, *types):
        self._listeners = []

    def connect(self, listener):
        self._listeners.append(listener)

    def disconnect(self, listener):
        self._listeners.remove(listener)

    def emit(self, *args, **kwargs):
        for listener in self._listeners:
            listener(*args, **kwargs)

    def __iadd__(self, listener):
        self.connect(listener)
        return self
